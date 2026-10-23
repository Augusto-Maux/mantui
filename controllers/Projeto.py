from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Projeto, Equipe
from utils import db
from flask_login import current_user, login_required

bp_projeto = Blueprint("projeto", __name__, template_folder='templates')

@bp_projeto.route('/recovery')
@login_required
def recovery():
	projetos = Projeto.query.all()
	return render_template('projeto/projeto_recovery.html', projetos=projetos)

@bp_projeto.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		equipes = Equipe.query.all()
		return render_template('projeto/projeto_add.html', equipes=equipes)
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		descricao = request.form.get('descricao')
		fk_id_user = current_user.id
		fk_id_equipe = request.form.get('fk_id_equipe')
		projeto = Projeto(nome, descricao, fk_id_user, fk_id_equipe)
		db.session.add(projeto)
		db.session.commit()
		return redirect(url_for('projeto.recovery'))
	
	else:
		return "Acesso inválido"

@bp_projeto.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	projeto = Projeto.query.get(id)
	if request.method=="GET":
		return render_template('projeto/projeto_update.html', projeto=projeto)
	
	elif request.method=="POST":
		projeto.nome = request.form.get('nome')
		projeto.descricao = request.form.get('descricao')
		db.session.add(projeto)
		db.session.commit()
		return redirect(url_for('projeto.recovery'))
	
	else:
		return "Acesso inválido"

@bp_projeto.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		return redirect(url_for('projeto.recovery'))

	try:
		projeto = Projeto.query.get(id)
		db.session.delete(projeto)
		db.session.commit()
		flash("Dados excluídos!", "success")

	except Exception as e:
		flash("Não foi possível excluir o projeto", "danger")

	return redirect(url_for('projeto.recovery'))