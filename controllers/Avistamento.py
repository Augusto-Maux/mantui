from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Avistamento, Especie
from utils import db
from flask_login import login_required, current_user

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

		# problema na adição do fk id usuário (16/10 - 17h10)
		fk_id_user = current_user.id
		fk_id_especie = request.form.get('fk_id_especie')
		
		avistamento = Avistamento(nome, latitude, longitude, bioma, tipo_registro, cond_ventos, cond_clima, observacoes, fk_id_user, fk_id_especie)
		db.session.add(avistamento)
		db.session.commit()
		return redirect(url_for('avistamento.recovery'))
	
	else:
		return "Acesso inválido"

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
		flash("Dados excluídos!", "success")

	except Exception as e:
		flash("Não foi possível excluir usuário", "danger")

	return redirect(url_for('avistamento.recovery'))