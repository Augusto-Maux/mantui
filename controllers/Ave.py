from flask import Blueprint, render_template, request, redirect, url_for
from models import Ave
from utils import db

bp_ave = Blueprint("ave", __name__, template_folder='templates')

@bp_ave.route('/recovery')
def recovery():
	aves = Ave.query.all()
	return render_template('ave_recovery.html', ave=aves)

@bp_ave.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == "GET":
		return render_template('ave_add.html')

	elif request.method == "POST":
		nome = request.form.get('nome')
		caracteristicas = request.form.get('caracteristicas')
		sexo = request.form.get('sexo')

		ave = Ave(nome, caracteristicas, sexo)

		db.session.add(ave)
		db.session.commit()

		return redirect(url_for('ave.recovery'))

	else:
		return "Acesso inválido"

@bp_ave.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	ave = Ave.query.get(id)
	if request.method == "GET":
		return render_template('ave_update.html', ave=ave)

	elif request.method == "POST":
		ave.nome = request.form.get('nome')
		ave.caracteristicas = request.form.get('caracteristicas')
		ave.sexo = request.form.get('sexo')

		db.session.commit()

		return redirect(url_for('ave.recovery'))

	else:
		return "Acesso inválido"

@bp_ave.route('/delete/<int:id>')
def delete(id):
	ave = Ave.query.get(id)

	db.session.delete(ave)
	db.session.commit()

	return "Dados excluídos"