from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Especie, StatusConservacao
from utils import db
from flask_login import current_user, login_required

bp_especie = Blueprint("especie", __name__, template_folder='templates')

@bp_especie.route('/recovery')
@login_required
def recovery():
	especies = Especie.query.all()
	return render_template('especie/especie_recovery.html', especies=especies)

@bp_especie.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		status_conservacao = StatusConservacao.query.all()
		return render_template('especie/especie_add.html', status_conservacao=status_conservacao)
	
	elif request.method=="POST":
		nome_comum = request.form.get('nome_comum')
		nome_cientifico = request.form.get('nome_cientifico')
		fk_id_status_conservacao = request.form.get('fk_id_status_conservacao')
		especie = Especie(nome_comum, nome_cientifico, fk_id_status_conservacao)
		db.session.add(especie)
		db.session.commit()
		return redirect(url_for('especie.recovery'))
	
	else:
		return "Acesso inválido"

@bp_especie.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	especie = Especie.query.get(id)
	if request.method=="GET":
		return render_template('especie/especie_update.html', especie=especie)
	
	elif request.method=="POST":
		especie.nome_comum = request.form.get('nome_comum')
		especie.nome_cientifico = request.form.get('nome_cientifico')
		especie.fk_id_status_conservacao = request.form.get('fk_id_status_conservacao')
		db.session.add(especie)
		db.session.commit()
		return redirect(url_for('especie.recovery'))
	
	else:
		return "Acesso inválido"

@bp_especie.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		return redirect(url_for('especie.recovery'))

	try:
		especie = Especie.query.get(id)
		db.session.delete(especie)
		db.session.commit()
		flash("Espécie excluída!", "success")

	except Exception as e:
		flash("Não foi possível excluir a espécie", "danger")

	return redirect(url_for('especie.recovery'))