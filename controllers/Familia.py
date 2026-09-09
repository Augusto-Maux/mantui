from flask import Blueprint, render_template, request, redirect, url_for
from models import Familia
from utils import db

bp_familia = Blueprint("familia", __name__, template_folder='templates')

@bp_familia.route('/recovery')
def recovery():
	familia = Familia.query.all()
	return render_template('familia_recovery.html', familia=familia)

@bp_familia.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=="GET":
		return render_template('familia_add.html')
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		caracteristicas = request.form.get('caracteristicas')
		familia = Familia(nome, caracteristicas)
		db.session.add(familia)
		db.session.commit()
		return redirect(url_for('familia.recovery'))
	
	else:
		return "Acesso inválido"

@bp_familia.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	familia = Familia.query.get(id)
	if request.method=="GET":
		return render_template('familia_update.html', status_conservacao=status_conservacao)
	
	elif request.method=="POST":
		familia.nome = request.form.get('nome')
		familia.caracteristicas = request.form.get('caracteristicas')
		db.session.add(familia)
		db.session.commit()
		return redirect(url_for('familia.recovery'))
	
	else:
		return "Acesso inválido"

@bp_familia.route('/delete/<int:id>')
def delete(id):
	familia = Familia.query.get(id)
	db.session.delete(familia)
	db.session.commit()
	return "Dados excluídos"