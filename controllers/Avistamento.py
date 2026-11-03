from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, current_app
from models import Avistamento, Especie
from utils import db
from weasyprint import HTML
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid

EXTENSOES = {'png', 'jpg', 'jpeg', 'webp', 'audio/*'}

bp_avistamento = Blueprint("avistamento", __name__, template_folder='templates')

@bp_avistamento.route('/recovery')
@login_required
def recovery():
	avistamento = Avistamento.query.all()
	return render_template('avistamento/avistamento_recovery.html', avistamento=avistamento)

@bp_avistamento.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		especies = Especie.query.all()
		return render_template('avistamento/avistamento_add.html', especies=especies)
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		latitude = request.form.get('latitude')
		longitude = request.form.get('longitude')
		bioma = request.form.get('bioma')
		tipo_registro = request.form.get('tipo_registro')
		cond_clima = request.form.get('cond_clima')
		cond_ventos = request.form.get('cond_ventos')
		observacoes = request.form.get('observacoes')
		data_hora = request.form.get('data_hora') # Falta colocar no html
		# Uploads - Falta Testar - Simplificar (Mídias)
		imagem = request.files.get('imagem')
		audio = request.files.get('audio')
		
		if imagem and imagem.filename:
			nome = secure_filename(imagem.filename)
			extensao = nome.rsplit('.', 1)[-1].lower()
					
			if extensao not in EXTENSOES:
				flash('Formato de imagem inválido.', 'danger')
				return redirect(url_for('avistamento.add'))
		
			new_name = f"{uuid.uuid4().hex}.{extensao}"
			caminho_salvar = os.path.join(
				current_app.config['UPLOAD_FOLDER'],
				new_name
			)
		
			imagem.save(caminho_salvar)
			caminho_imagem = f"uploads/avistamentos/{new_name}"

		midias = caminhos
		fk_id_user = current_user.id
		fk_id_especie = request.form.get('fk_id_especie')
		
		avistamento = Avistamento(nome, latitude, longitude, bioma, tipo_registro, cond_ventos, cond_clima, observacoes, imagem, audio, fk_id_user, fk_id_especie)
		db.session.add(avistamento)
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

@bp_avistamento.route('/pdf')
@login_required
def avistamentos_pdf():
    avistamentos = Avistamento.query.all()
    html = render_template('relatorio/avistamentos.html', avistamentos=avistamentos)
    pdf = HTML(string=html).write_pdf()
    resposta = make_response(pdf)
    resposta.headers['Content-Type'] = 'application/pdf'
    return resposta