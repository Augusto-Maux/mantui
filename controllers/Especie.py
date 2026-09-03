from flask import Blueprint, render_template, request, redirect, url_for
from models import Especie
from utils import db

bp_especie = Blueprint("especie", __name__, template_folder='templates')

@bp_especie.route('/recovery')
def recovery():
	especies = Especie.query.all()
	return render_template('especie_recovery.html', especie=especies)

@bp_especie.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=="GET":
		return render_template('especie_add.html')
	
	elif request.method=="POST":
		nome_comum = request.form.get('nome_comum')
		nome_cientifico = request.form.get('nome_cientifico')
		especie = Especie(nome_comum, nome_cientifico)
		db.session.add(especie)
		db.session.commit()
		return redirect(url_for('especie.recovery'))
	
	else:
		return "Acesso inválido"

@bp_especie.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	especie = Especie.query.get(id)
	if request.method=="GET":
		return render_template('especie_update.html', e=especie)
	
	elif request.method=="POST":
		especie.nome = request.form.get('nome')
		especie.email = request.form.get('email')
		db.session.add(especie)
		db.session.commit()
		return redirect(url_for('especie.recovery'))
	
	else:
		return "Acesso inválido"

@bp_especie.route('/delete/<int:id>')
def delete(id):
	especie = Especie.query.get(id)
	db.session.delete(especie)
	db.session.commit()
	return "Dados excluídos"