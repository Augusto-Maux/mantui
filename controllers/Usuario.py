from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import Usuario
from utils import db, lm
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os, uuid

EXTENSOES = {'png', 'jpg', 'jpeg', 'webp'}

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/recovery')
@login_required
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
		username = request.form.get('username')
		# criar entidade para CidadaoCientista, Administrador e Moderador
		papel = "Cidadão Cientista"
		# foto_perfil = request.files.get('foto_perfil')

		u = Usuario(nome, email, senha, idade, username, papel)
		db.session.add(u)
		db.session.commit()
		login_user(u)

		flash('Cadastro Realizado!', 'success')
		return redirect(url_for('usuario.recovery'))
	
	else:
		flash('Problema no Cadastro', 'danger')
		return redirect(url_for('usuario.add'))

# falta redefinição de senha (16/10 - 17h55)
@bp_usuario.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	user = Usuario.query.get(id)
	if request.method=="GET":
		return render_template('usuario/usuario_update.html', user=user)
	
	elif request.method=="POST":
		user.nome = request.form.get('nome')
		user.email = request.form.get('email')
		
		# user.foto_perfil = request.files.get('foto_perfil')
		foto_perfil = request.files.get('foto_perfil')
		caminho = user.foto_perfil

		if foto_perfil and foto_perfil.filename:
			nome = secure_filename(foto_perfil.filename)
			extensao = nome.rsplit('.', 1)[-1].lower()
			
			if extensao not in EXTENSOES:
				return 'Formato sem permissão', 400

			new_name = f"{uuid.uuid4().hex}.{extensao}"
			caminho = os.path.join(
				current_app.config['UPLOAD_FOLDER'],
				new_name
			)

			foto_perfil.save(caminho)
			caminho = f"uploads/usuarios/{new_name}"

		user.foto_perfil = caminho
		
		db.session.add(user)
		db.session.commit()
		flash('Atualização realizada!', 'success')
		return redirect(url_for('usuario.recovery'))
	
	else:
		flash('Problema na atualização', 'danger')
		return redirect(url_for('usuario.recovery'))

@bp_usuario.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		return redirect(url_for('usuario.recovery'))

	try:
		usuario = Usuario.query.get(id)
		db.session.delete(usuario)
		db.session.commit()
		flash("Dados excluídos!", "success")
		
	except Exception as e:
		flash("Não foi possível excluir usuário", "danger")
	return redirect(url_for('usuario.recovery'))

# AUTH
@lm.user_loader
def load_user(id):
	usuario = Usuario.query.filter_by(id=id).first()
	return usuario

@bp_usuario.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('usuario/login.html')

	email = request.form.get('email')
	senha = request.form.get('senha')

	usuario = Usuario.query.filter_by(email = email).first()

	if usuario and usuario._verificar_senha(senha):
		login_user(usuario)
		flash('Login realizado!', 'success')
		return redirect(url_for('usuario.recovery'))
	
	else:
		flash('Dados não encontrados.', 'danger')
		return redirect(url_for('usuario.login'))

@bp_usuario.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	flash('Sessão encerrada', 'info')
	return redirect(url_for('usuario.login'))