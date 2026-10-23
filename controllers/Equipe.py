from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Equipe
from utils import db
from flask_login import current_user, login_required

bp_equipe = Blueprint("equipe", __name__, template_folder='templates')

@bp_equipe.route('/recovery')
@login_required
def recovery():
	equipes = Equipe.query.all()
	return render_template('equipe/equipe_recovery.html', equipes=equipes)

@bp_equipe.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		return render_template('equipe/equipe_add.html')
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		fk_id_user = current_user.id
		equipe = Equipe(nome, fk_id_user)
		db.session.add(equipe)
		db.session.commit()
		flash('Equipe Adicionada!')
		return redirect(url_for('equipe.recovery'))
	
	else:
		return "Acesso inválido"

@bp_equipe.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	equipe = Equipe.query.get(id)
	if request.method=="GET":
		return render_template('equipe/equipe_update.html', equipe=equipe)
	
	elif request.method=="POST":
		equipe.nome = request.form.get('nome')
		db.session.add(equipe)
		db.session.commit()
		return redirect(url_for('equipe.recovery'))
	
	else:
		return "Acesso inválido"

@bp_equipe.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		return redirect(url_for('equipe.recovery'))

	try:
		equipe = Equipe.query.get(id)
		db.session.delete(equipe)
		db.session.commit()
		flash("Equipe excluída!", "success")

	except Exception as e:
		flash("Não foi possível excluir a equipe", "danger")

	return redirect(url_for('equipe.recovery'))