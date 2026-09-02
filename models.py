from utils import db, relationship
from datetime import date, datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    status_conta = db.Column(db.Boolean, default=True)
    papel = db.Column(db.String(100))
    foto_perfil = db.Column(db.String(100), unique=True)
    projetos = relationship('Projeto', back_populates='user')
    equipes = relationship('Equipe', back_populates='user')

    # create __init__ function here

    def def_senha(self, senha_without_hash):
        self.senha = generate_password_hash(senha_without_hash)

    def verificar_senha(self, senha_without_hash):
        return check_password_hash(self.senha, senha_without_hash)
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Projeto(db.Model):
    __tablename__= "projetos"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date, default=date.today)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    user = relationship('Usuario', back_populates='projetos')
    equipes = relationship('Equipe', back_populates='projeto')
    # membros, quant_mebros, quant_equipes

    # create __init__ function here

class Equipe(db.Model):
    __tablename__= "equipes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    data_criacao = db.Column(db.Date, default=date.today)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    fk_id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    user = relationship('Usuario', back_populates='equipes')
    projeto = relationship('Projeto', back_populates='equipes')

class Avistamento(db.Model):
    __tablename__= "avistamento"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    bioma = db.Column(db.String(200))
    tipo_registro = db.Column(db.String(200))
    cond_clima = db.Column(db.String(200))
    cond_ventos = db.Column(db.String(200))
    observacoes = db.Column(db.String(300))
    data_hora = db.Column(db.Datetime(timezone=True), nullable=False)

class Especie(db.Model):
    __tablename__ = "especie"
    id = db.Column(db.Integer, primary_key=True)
    nome_comum = db.Column(db.String(200))
    nome_cientifico = db.Column(db.String(200))
    audio = db.Column(db.String(300))
    imagem = db.Column(db.String(300))