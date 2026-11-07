from utils import db
from datetime import date, datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Avistamento <-> Pesquisadores
avistamento_pesquisador = db.Table('Avistamento_Pesquisador',
    db.Column('id_avistamento', db.Integer, db.ForeignKey('avistamento.id'), primary_key=True),
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
)

# Membros <-> Equipe
# colocar CASCADE
membros_equipe = db.Table('Membros_Equipe',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('id_equipe', db.Integer, db.ForeignKey('equipe.id'), primary_key=True)               
)

class Usuario(db.Model, UserMixin):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Date) # podia ter cálculo
    username = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(100))
    foto_perfil = db.Column(db.String(500), unique=True)
    comprovante_membro = db.Column(db.String(500), nullable=True) # exclusivo para tornar_moderador

    def __init__(self, nome, email, senha_text, idade, username, papel):
        self.nome = nome
        self.email = email
        self.senha = self._def_senha(senha_text)
        self.idade = idade
        self.username = username
        self.papel = papel

    def _def_senha(self, senha_without_hash):
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
    fk_id_equipe = db.Column(db.Integer, db.ForeignKey('equipe.id'))

    user = db.relationship('Usuario', foreign_keys=fk_id_user)
    equipe = db.relationship('Equipe', back_populates='projetos')

    def __init__(self, nome, descricao, fk_id_user, fk_id_equipe):
        self.nome = nome
        self.descricao = descricao
        self.fk_id_user = fk_id_user
        self.fk_id_equipe = fk_id_equipe\

    def __repr__(self):
        return f"<Projeto {self.nome}>"

class Equipe(db.Model):
    __tablename__= "equipe"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    data_criacao = db.Column(db.Date, default=date.today)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))    
    user = db.relationship('Usuario', foreign_keys=fk_id_user)
    projetos = db.relationship('Projeto', back_populates='equipe')

    membros = db.relationship('Usuario', secondary=membros_equipe, backref='equipes')

    def __init__(self, nome, fk_id_user):
        self.nome = nome
        self.fk_id_user = fk_id_user

    def __repr__(self):
        return f"<Equipe {self.nome}>"

class Avistamento(db.Model):
    __tablename__= "avistamento"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    latitude = db.Column(db.String(200))
    longitude = db.Column(db.String(200))
    bioma = db.Column(db.String(200))
    tipo_registro = db.Column(db.String(200))
    cond_clima = db.Column(db.String(200))
    cond_ventos = db.Column(db.String(200))
    observacoes = db.Column(db.String(300))
    data_hora = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))

    # relacionamento usuário (principal pesquisador)
    fk_id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    user = db.relationship('Usuario', foreign_keys=fk_id_user)

    # relacionamento espécie
    fk_id_especie = db.Column(db.Integer, db.ForeignKey('especie.id'))
    especie = db.relationship('Especie', foreign_keys=fk_id_especie)

    # relacionamento para pesquisador adicional
    pesquisadores_adicionais = db.relationship('Usuario', secondary=avistamento_pesquisador, backref='avistamentos_compartilhados')

    # relacionamento com mídias
    midias = db.relationship('Midia', back_populates='avistamento')

    def __init__(self, nome, bioma, tipo_registro, cond_clima, cond_ventos, observacoes, fk_id_user, fk_id_especie, latitude, longitude, data_hora):
        self.nome = nome
        self.bioma = bioma
        self.tipo_registro = tipo_registro
        self.cond_clima = cond_clima
        self.cond_ventos = cond_ventos
        self.observacoes = observacoes
        self.fk_id_user = fk_id_user
        self.fk_id_especie = fk_id_especie
        self.latitude = latitude
        self.longitude = longitude
        if data_hora:
            self.data_hora = data_hora

    def __repr__(self):
        return f"<Avistamento {self.nome}>"

# aprimorar Midia (atributos) posteriormente
class Midia(db.Model):
    __tablename__ = "midia"
    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(300), nullable=False)
    data_upload = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))

    # relacionamento com avistamentos
    fk_id_avistamento = db.Column(db.Integer, db.ForeignKey('avistamento.id'), nullable=False)
    avistamento = db.relationship('Avistamento', back_populates='midias')

    def __init__(self, caminho, fk_id_avistamento):
        self.caminho = caminho
        self.fk_id_avistamento = fk_id_avistamento

    def __repr__(self):
        return f"<Mídia {self.caminho}>"

class Especie(db.Model):
    __tablename__ = "especie"
    id = db.Column(db.Integer, primary_key=True)
    nome_comum = db.Column(db.String(200))
    nome_cientifico = db.Column(db.String(200))
    # audio = db.Column(db.String(300))
    # imagem = db.Column(db.String(300)) - UPLOAD DE IMAGENS
    fk_id_status_conservacao = db.Column(db.Integer, db.ForeignKey('status_conservacao.id'))
    status_conservacao = db.relationship('StatusConservacao', foreign_keys=fk_id_status_conservacao)

    def __init__(self, nome_comum, nome_cientifico, fk_id_status_conservacao):
        self.nome_comum = nome_comum
        self.nome_cientifico = nome_cientifico
        self.fk_id_status_conservacao = fk_id_status_conservacao

    def __repr__(self):
        return f"<Especie {self.nome_comum} {self.nome_cientifico}>"

class StatusConservacao(db.Model):
    __tablename__ = "status_conservacao"
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(300))
    data_avaliacao = db.Column(db.Date, default=date.today)
    fonte = db.Column(db.String(300))
    descricao = db.Column(db.String(300))
    observacoes = db.Column(db.String(300))

    def __init__(self, descricao, categoria, observacoes, fonte):
        self.descricao = descricao
        self.categoria = categoria
        self.observacoes = observacoes
        self.fonte = fonte

    def __repr__(self):
        return f"<Status Conservação {self.descricao}>"

# Notificação - classe