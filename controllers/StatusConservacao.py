from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import StatusConservacao
from utils import db
from flask_login import login_required, current_user

bp_status = Blueprint("status_conservacao", __name__, template_folder='templates')

@bp_status.route('/recovery')
@login_required
def recovery():
	status_conservacao = StatusConservacao.query.all()
	return render_template('status_conservacao/status_conservacao_recovery.html', status_conservacao=status_conservacao)

@bp_status.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method=="GET":
		return render_template('status_conservacao/status_conservacao_add.html')
	
	elif request.method=="POST":
		descricao = request.form.get('descricao')
		categoria = request.form.get('categoria')
		observacoes = request.form.get('observacoes')
		fonte = request.form.get('fonte')
		status_conservacao = StatusConservacao(descricao, categoria, observacoes, fonte)
		db.session.add(status_conservacao)
		db.session.commit()
		return redirect(url_for('status_conservacao.recovery'))
	
	else:
		return "Acesso inválido"

@bp_status.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	status_conservacao = StatusConservacao.query.get(id)
	if request.method=="GET":
		return render_template('status_conservacao/status_conservacao_update.html', status_conservacao=status_conservacao)
	
	elif request.method=="POST":
		status_conservacao.descricao = request.form.get('descricao')
		status_conservacao.categoria = request.form.get('categoria')
		status_conservacao.observacoes = request.form.get('observacoes')
		status_conservacao.fonte = request.form.get('fonte')
		db.session.add(status_conservacao)
		db.session.commit()
		return redirect(url_for('status_conservacao.recovery'))
	
	else:
		return "Acesso inválido"

@bp_status.route('/delete/<int:id>')
@login_required
def delete(id):
	if current_user.papel not in ['Administrador', 'Moderador']:
		flash("Sem acesso", "danger")
		return redirect(url_for('projeto.recovery'))

	try:
		status_conservacao = StatusConservacao.query.get(id)
		db.session.delete(status_conservacao)
		db.session.commit()
		flash("Dados excluídos!", "success")

	except Exception as e:
		flash("Não foi possível excluir o Status", "danger")

	return redirect(url_for('status_conservacao.recovery'))