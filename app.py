import os
from flask import Flask
from flask import render_template
from utils import db, lm
from dotenv import load_dotenv
from flask_migrate import Migrate
import logging

from controllers.Usuario import bp_usuario
from controllers.Projeto import bp_projeto
from controllers.Equipe import bp_equipe
from controllers.Avistamento import bp_avistamento
from controllers.Especie import bp_especie
from controllers.StatusConservacao import bp_status

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s: %(message)s]'
)

load_dotenv()

app = Flask(__name__)

app.register_blueprint(bp_usuario, url_prefix='/usuario')
app.register_blueprint(bp_projeto, url_prefix='/projeto')
app.register_blueprint(bp_equipe, url_prefix='/equipe')
app.register_blueprint(bp_avistamento, url_prefix='/avistamento')
app.register_blueprint(bp_especie, url_prefix='/especie')
app.register_blueprint(bp_status, url_prefix='/status_conservacao')

@app.route('/')
def first_page():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('erro404.html'), 404

app.config["EBIRD_API_KEY"] = os.getenv("EBIRD_API_KEY")

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"

# app.secret_key = ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

lm.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)