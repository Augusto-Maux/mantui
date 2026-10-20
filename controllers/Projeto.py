from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Projeto
from utils import db

bp_projeto = Blueprint("projeto", __name__, template_folder='templates')

# OK
@bp_projeto.route('/recovery')
def recovery():
	projetos = Projeto.query.all()
	return render_template('projeto/projeto_recovery.html', projetos=projetos)

@bp_projeto.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=="GET":
		return render_template('projeto/projeto_add.html')
	
	elif request.method=="POST":
		nome = request.form.get('nome')
		descricao = request.form.get('descricao')
		projeto = Projeto(nome, descricao)

		# flash messages
		db.session.add(projeto)
		db.session.commit()
		return redirect(url_for('projeto.recovery'))
	
	else:
		return "Acesso inválido"

@bp_projeto.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	projeto = Projeto.query.get(id)
	if request.method=="GET":
		return render_template('projeto/projeto_update.html', projeto=projeto)
	
	elif request.method=="POST":
		projeto.nome = request.form.get('nome')
		projeto.descricao = request.form.get('descricao')

		# flash messages
		db.session.add(projeto)
		db.session.commit()
		return redirect(url_for('projeto.recovery'))
	
	else:
		return "Acesso inválido"

@bp_projeto.route('/delete/<int:id>')
def delete(id):
	projeto = Projeto.query.get(id)
	db.session.delete(projeto)
	db.session.commit()

	# mudar para flash messages
	return "Dados excluídos"