from utils import db
from datetime import date, datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Integer)
    # status_conta = db.Column(db.Boolean, default=True)
    papel = db.Column(db.String(100))
    foto_perfil = db.Column(db.String(100), unique=True)

    def __init__(self, nome, email, senha_text, idade, papel):
        self.nome = nome
        self.email = email
        self.senha = self._def_senha(senha_text)
        self.idade = idade
        self.papel = papel

    def _def_senha(self, senha_without_hash):
        # self.senha = generate_password_hash(senha_without_hash)
        return generate_password_hash(senha_without_hash)

    def _verificar_senha(self, senha_without_hash):
        return check_password_hash(self.senha, senha_without_hash)
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Projeto(db.Model):
    __tablename__= "projetos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date, default=date.today)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    user = db.relationship('Usuario', foreign_keys=fk_id_user)

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f"<Projeto {self.nome}>"

class Equipe(db.Model):
    __tablename__= "equipes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    data_criacao = db.Column(db.Date, default=date.today)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    fk_id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    user = db.relationship('Usuario', foreign_keys=fk_id_user)
    projeto = db.relationship('Projeto', foreign_keys=fk_id_projeto)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"<Equipe {self.nome}>"

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
    data_hora = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, nome, latitude, longitude, bioma, tipo_registro, cond_clima, cond_ventos, observacoes):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude
        self.bioma = bioma
        self.tipo_registro = tipo_registro
        self.cond_clima = cond_clima
        self.cond_ventos = cond_ventos
        self.observacoes = observacoes

    def __repr__(self):
        return f"<Avistamento {self.nome}>"

class Especie(db.Model):
    __tablename__ = "especie"
    id = db.Column(db.Integer, primary_key=True)
    nome_comum = db.Column(db.String(200))
    nome_cientifico = db.Column(db.String(200))
    audio = db.Column(db.String(300))
    imagem = db.Column(db.String(300))

    def __init__(self, nome_comum, nome_cientifico):
        self.nome_comum = nome_comum
        self.nome_cientifico = nome_cientifico

    def __repr__(self):
        return f"<Especie {self.nome_comum} {self.nome_cientfico}>"