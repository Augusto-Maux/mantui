from flask import render_template
from utils import db
from flask import Blueprint

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')