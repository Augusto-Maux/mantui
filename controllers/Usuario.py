from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import Usuario
from utils import db, lm
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os, uuid

EXTENSOES = {'png', 'jpg', 'jpeg', 'webp'}

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/home')
@login_required
def home():
    usuarios = Usuario.query.all()
    return render_template('home.html', usuarios=usuarios)

@bp_usuario.route('/notificacoes')
@login_required
def notificacoes():
    return render_template('notificacoes.html', user=current_user)

@bp_usuario.route('/perfil')
@login_required
def perfil():
    return render_template('usuario/perfil.html', user=current_user)

@bp_usuario.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "GET":
        return render_template('usuario/cadastro.html')
    
    elif request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        idade = request.form.get('idade')
        username = request.form.get('username')
        papel = "Cidadão Cientista"

        u = Usuario(nome, email, senha, idade, username, papel)
        db.session.add(u)
        db.session.commit()
        login_user(u)

        flash('Cadastro Realizado!', 'success')
        return redirect(url_for('usuario.home'))
    
    else:
        flash('Problema no Cadastro', 'danger')
        return redirect(url_for('usuario.add'))

@bp_usuario.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user = Usuario.query.get(id)
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('usuario.home'))

    if request.method == "GET":
        return render_template('usuario/usuario_update.html', user=user)
    
    elif request.method == "POST":
        user.nome = request.form.get('nome')
        user.email = request.form.get('email')
        
        foto_perfil = request.files.get('foto_perfil')
        caminho = user.foto_perfil

        if foto_perfil and foto_perfil.filename:
            pasta = os.path.join(current_app.static_folder, 'uploads', 'usuarios')
            os.makedirs(pasta, exist_ok=True)

            nome = secure_filename(foto_perfil.filename)
            extensao = nome.rsplit('.', 1)[-1].lower()
            
            if extensao not in EXTENSOES:
                flash('Formato de imagem inválido.', 'danger')
                return redirect(url_for('usuario.update', id=id))

            new_name = f"{uuid.uuid4().hex}.{extensao}"
            caminho_salvar = os.path.join(
                pasta,
                new_name
            )

            foto_perfil.save(caminho_salvar)
            caminho = f"uploads/usuarios/{new_name}"

        user.foto_perfil = caminho
        db.session.commit()
        
        flash('Atualização realizada!', 'success')
        return redirect(url_for('usuario.home'))
    
    else:
        flash('Problema na atualização', 'danger')
        return redirect(url_for('usuario.home'))

@bp_usuario.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.papel not in ['Administrador', 'Moderador']:
        flash("Sem acesso", "danger")
        return redirect(url_for('usuario.home'))

    try:
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            flash("Dados excluídos!", "success")
        else:
            flash("Usuário não encontrado", "warning")
    except Exception as e:
        db.session.rollback()
        flash("Não foi possível excluir usuário", "danger")
        
    return redirect(url_for('usuario.home'))

@bp_usuario.route('/tornar_moderador', methods=['GET', 'POST'])
@login_required
def tornar_moderador():
    if current_user.papel not in ['Administrador', 'Moderador']:
        flash("Sem acesso", "danger")
        return redirect(url_for('usuario.home'))

    if request.method == "GET":
        usuarios = Usuario.query.all()
        return render_template('usuario/tornar_moderador.html', usuarios=usuarios)

    elif request.method == "POST":
        id = request.form.get('id')
        usuario = Usuario.query.filter_by(id=id).first()

        if usuario:
            usuario.papel = 'Moderador'
            db.session.commit()
            flash('Usuário atualizado para Moderador!', 'success')
            return redirect(url_for('usuario.home'))
        else:
            flash('Dados não encontrados.', 'danger')
            return redirect(url_for('usuario.tornar_moderador'))

    else:
        flash('Problema ao tornar moderador', 'danger')
        return redirect(url_for('usuario.home'))

# AUTH
@lm.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@bp_usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('usuario/login.html')

    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario._verificar_senha(senha):
        login_user(usuario)
        flash('Login realizado!', 'success')
        # Redireciona para usuario.home, renderizando home.html com a URL /usuario/home
        return redirect(url_for('usuario.home'))
    else:
        flash('Dados não encontrados.', 'danger')
        return redirect(url_for('usuario.login'))

@bp_usuario.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Sessão encerrada', 'info')
    return redirect(url_for('usuario.login'))