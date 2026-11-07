from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Equipe, Usuario, Notificacao
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


@bp_equipe.route('/convidar/<int:id>', methods=['POST'])
@login_required
def convidar(id):
	equipe = Equipe.query.get_or_404(id)

	if equipe.fk_id_user != current_user.id:
		flash('Você não pode convidar usuários')
		return redirect(url_for('usuario.home'))

	username_convidado = request.form.get('username')
	username_convidado = Usuario.query.filter_by(username=username_convidado).first()

	if not username_convidado:
		flash('Usuário não encontrado')
		return redirect(url_for('usuario.home'))

	if (username_convidado in equipe.membros) or (username_convidado == equipe.fk_id_user):
		flash('O usuário já faz parte do grupo')
		return redirect(url_for('usuario.home'))

	convite_existente = Notificacao.query.filter_by(
		fk_id_user=username_convidado.id,
		fk_id_equipe=equipe.id
	).first()

	if convite_existente:
		flash(f'O convite deste grupo ao {username_convidado} já existe.')
		return redirect(url_for('usuario.home'))

	mensagem = f"O pesquisador {current_user.username} convidou você!"
	notificacao = Notificacao(mensagem, username_convidado.id, equipe.id)

	db.session.add(notificacao)
	db.session.commit()

	flash('Notificação Enviada!')
	return redirect(url_for('usuario.home'))

# resposta - convite