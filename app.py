from flask import Flask
from utils import db
import os
from flask_migrate import Migrate
from models import Usuario, Projeto, Equipe, Avistamento, Especie

from controllers.Usuario import bp_usuario
from controllers.Projeto import bp_projeto
from controllers.Equipe import bp_equipe
from controllers.Avistamento import bp_avistamento
from controllers.Especie import bp_especie

app = Flask(__name__)

app.register_blueprint(bp_usuario, url_prefix='/usuario')
app.register_blueprint(bp_projeto, url_prefix='/projeto')
app.register_blueprint(bp_equipe, url_prefix='/equipe')
app.register_blueprint(bp_avistamento, url_prefix='/avistamento')
app.register_blueprint(bp_especie, url_prefix='/especie')


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"

print(conexao)
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)