from flask import Flask
from utils import db

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    status_conta = db.Column(db.Boolean())
    cargo = db.Column(db.String(100))

    def __init__(self, nome, email, senha, idade, status_conta, cargo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idade = idade
        self.status_conta = status_conta
        self.cargo = cargo
    
    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Projeto(db.Model):
    __tablename__= "projeto"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date)
    membros = db.Column(db.String(300))

    def __init__(self, nome, descricao, data_criacao, membros):
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = data_criacao
        self.membros = membros