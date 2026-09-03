from flask import Blueprint, render_template, request, redirect, url_for
from models import Equipe
from utils import db

bp_equipe = Blueprint("equipe", __name__, template_folder='templates')

@bp_equipe.route('/recovery')
def recovery():
	equipes = Equipe.query.all()
	return render_template('equipe_recovery.html', equipe=equipes)

@bp_equipe.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=="GET":
		return render_template('equipe_add.html')
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		equipe = Equipe(nome)
		db.session.add(equipe)
		db.session.commit()
		return redirect(url_for('equipe.recovery'))
	
	else:
		return "Acesso inválido"

@bp_equipe.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	equipe = Equipe.query.get(id)
	if request.method=="GET":
		return render_template('equipe_update.html', e=equipe)
	
	elif request.method=="POST":
		equipe.nome = request.form.get('nome')
		db.session.add(equipe)
		db.session.commit()
		return redirect(url_for('equipe.recovery'))
	
	else:
		return "Acesso inválido"

@bp_equipe.route('/delete/<int:id>')
def delete(id):
	equipe = Equipe.query.get(id)
	db.session.delete(equipe)
	db.session.commit()
	return "Dados excluídos"