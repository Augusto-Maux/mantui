from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, current_app
from models import Avistamento, Especie, Midia, Usuario
from utils import db
from weasyprint import HTML
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os, uuid

# aumentar quantidade de extensões
EXTENSOES = {'png', 'jpg', 'jpeg', 'webp', 'mp4', 'mp3', 'wav'}

bp_avistamento = Blueprint("avistamento", __name__, template_folder='templates')

def salvar_midias_uploads(arquivos, id_avistamento):
	# realizar pasta de uploads para usuarios em Usuario.py

	pasta = os.path.join(current_app.static_folder, 'uploads', 'midias')
	os.makedirs(pasta, exist_ok=True)

	for a in arquivos:
		if a and a.filename:
			nome_arquivo = secure_filename(a.filename)
			extensao = nome_arquivo.rsplit('.', 1)[-1].lower()
			nome = f"{uuid.uuid4()}.{extensao}"
			caminho = os.path.join(pasta, nome)

			a.save(caminho)

			caminho_relativo = f"uploads/midias/{nome}"

			midia = Midia(caminho_relativo, id_avistamento)

			db.session.add(midia)

@bp_avistamento.route('/recovery')
@login_required
def recovery():
	avistamento = Avistamento.query.order_by(Avistamento.id.desc()).all()
	
	return render_template('avistamento/avistamento_recovery.html', avistamento=avistamento)

@bp_avistamento.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		especies = Especie.query.order_by(Especie.nome_comum).all()
		usuarios = Usuario.query.order_by(Usuario.nome).all()
		return render_template('avistamento/avistamento_add.html', especies=especies, usuarios=usuarios)
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		bioma = request.form.get('bioma')
		tipo_registro = request.form.get('tipo_registro')
		cond_clima = request.form.get('cond_clima')
		cond_ventos = request.form.get('cond_ventos')
		observacoes = request.form.get('observacoes')
		longitude = request.form.get('longitude')
		latitude = request.form.get('latitude')
		fk_id_user = current_user.id

		fk_id_especie = request.form.get('fk_id_especie') or None

		data_hora_string = request.form.get('data_hora')
		data_hora_formatado = None
		if data_hora_string:
			try:
				data_hora_formatado = datetime.strptime(data_hora_string, '%Y-%m-%dT%H:%M')
			except Exception:
				data_hora_formatado = datetime.utcnow()
		
		avistamento = Avistamento(nome, bioma, tipo_registro, cond_ventos, cond_clima, observacoes, fk_id_user, fk_id_especie, latitude, longitude, data_hora_formatado)
		

		# pesquisadores adicionais (Table) - falta adicionar essa lista no HTML
		id_pesquisadores = request.form.getlist('pesquisadores_adicionais')
		if id_pesquisadores:
			for id_pesquisador in id_pesquisadores:
				pesquisador = Usuario.query.get(id_pesquisador)
				if pesquisador:
					avistamento.pesquisadores_adicionais.append(pesquisador)

		db.session.add(avistamento)
		db.session.flush()

		# falta colocar isso no HTML
		arquivos = request.files.getlist('midia')
		salvar_midias_uploads(arquivos, avistamento.id)

		db.session.commit()

		flash('Avistamento Realizado!', 'success')
		return redirect(url_for('avistamento.recovery'))
	
	else:
		flash('Problema no Cadastro', 'danger')
		return redirect(url_for('avistamento.add'))

@bp_avistamento.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	avistamento = Avistamento.query.get(id)
	if request.method=="GET":
		return render_template('avistamento/avistamento_update.html', avistamento=avistamento)
	
	elif request.method=="POST":
		avistamento.nome = request.form.get('nome')
		avistamento.latitude = request.form.get('latitude')
		avistamento.longitude = request.form.get('longitude')
		avistamento.bioma = request.form.get('bioma')
		avistamento.tipo_registro = request.form.get('tipo_registro')
		avistamento.cond_clima = request.form.get('cond_clima')
		avistamento.cond_ventos = request.form.get('cond_ventos')
		avistamento.observacoes = request.form.get('observacoes')
		avistamento.fk_id_especie = request.form.get('fk_id_especie')
		db.session.add(avistamento)
		db.session.commit()
		flash('Atualização realizada!', 'success')
		return redirect(url_for('avistamento.recovery'))

	else:
		flash('Problema na atualização', 'danger')
		return redirect(url_for('avistamento.recovery'))

@bp_avistamento.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		
		return redirect(url_for('avistamento.recovery'))

	try:
		avistamento = Avistamento.query.get(id)
		db.session.delete(avistamento)
		db.session.commit()
		flash("Os dados do avistamento foram excluídos!", "success")

	except Exception as e:
		flash("Não foi possível excluir avistamento", "danger")

	return redirect(url_for('avistamento.recovery'))

@bp_avistamento.route('/pdf/<int:id>')
@login_required
def avistamento_pdf_individual(id):
    avistamento = Avistamento.query.get_or_404(id)
    html = render_template('relatorio/avistamentos.html', avistamentos=[avistamento])
    pdf = HTML(string=html).write_pdf()
    resposta = make_response(pdf)
    resposta.headers['Content-Type'] = 'application/pdf'
    return resposta