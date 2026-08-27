from flask import Flask
from utils import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    status_conta = db.Column(db.Boolean, default=True)
    cargo = db.Column(db.String(100))

    def def_senha(self, senha_without_hash):
        self.senha = generate_password_hash(senha_without_hash)

    def verificar_senha(self, senha_without_hash):
        return check_password_hash(self.senha, senha_without_hash)
    
    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Projeto(db.Model):
    __tablename__= "projeto"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date)
    # membros = db.Column(db.String(300))

    def __init__(self, nome, descricao, data_criacao, membros):
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = data_criacao
        self.membros = membros

class Avistamento(db.Model):
    __tablename__= "avistamento"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    localizacao = db.Column(db.String(200))
    observacoes = db.Column(db.String(300))
    data_hora = db.Column(db.Datetime(timezone=True), nullable=False)
    # add fk_anilha_id here

    def __init__(self, nome, localizacao, observacoes, data_hora):
        self.nome = nome
        self.localizacao = localizacao
        self.observacoes = observacoes
        self.data_hora = data_hora

class Ave(db.Model):
    __tablename__= "ave"
    id = db.Column(db.Integer, primary_key = True)
    nome_cientifico = db.Column(db.String(100))
    nome_comum = db.Column(db.String(100))
    especie = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    tipo_registro = db.Column(db.String(100))
    # add fk_id_avistamento 

    def __init__(self, nome_cientifico, nome_comum, especie, sexo, tipo_registro):
        self.nome_cientifico = nome_cientifico
        self.nome_comum = nome_comum
        self.especie = especie
        self.sexo = sexo
        self.tipo_registro = tipo_registro