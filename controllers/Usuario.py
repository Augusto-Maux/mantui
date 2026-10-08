from flask import Blueprint, render_template, request, redirect, url_for
from models import Usuario
from utils import db

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/recovery')
def recovery():
	usuarios = Usuario.query.all()
	return render_template('usuario/usuario_recovery.html', usuarios=usuarios)

@bp_usuario.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=="GET":
		return render_template('usuario/usuario_add.html')
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		email = request.form.get('email')
		senha = request.form.get('senha')
		idade = request.form.get('idade')
		papel = request.form.get('papel')
		u = Usuario(nome, email, senha, idade, papel)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('usuario.recovery'))
	
	else:
		return "Acesso inválido"

@bp_usuario.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	user = Usuario.query.get(id)
	if request.method=="GET":
		return render_template('usuario/usuario_update.html', user=user)
	
	elif request.method=="POST":
		user.nome = request.form.get('nome')
		user.email = request.form.get('email')
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('usuario.recovery'))
	
	else:
		return "Acesso inválido"

@bp_usuario.route('/delete/<int:id>')
def delete(id):
	usuario = Usuario.query.get(id)
	db.session.delete(usuario)
	db.session.commit()
	return "Dados excluídos"