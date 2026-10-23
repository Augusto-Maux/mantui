from flask import Blueprint, render_template, make_response
from models import Avistamento
from weasyprint import HTML
from flask_login import login_required

bp_relatorio = Blueprint("relatorio", __name__, template_folder='templates')

@bp_relatorio.route('/avistamentos/pdf')
@login_required
def avistamentos_pdf():
    avistamentos = Avistamento.query.all()
    html = render_template('relatorio/avistamentos.html', avistamentos=avistamentos)
    pdf = HTML(string=html).write_pdf()
    resposta = make_response(pdf)
    resposta.headers['Content-Type'] = 'application/pdf'
    return resposta