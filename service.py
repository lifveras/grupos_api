from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
flask_jwt = JWTManager()
db = SQLAlchemy()

def criar_tabelas():
        # Tabela de Usuários
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                senha VARCHAR(250) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """))
        
        # Tabela de Telefones (Relacionamento Um-para-Muitos com Usuario)
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS telefone (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                usuario_id INTEGER NOT NULL,
                ddd VARCHAR(2) NOT NULL,
                numero VARCHAR(20) NOT NULL,
                tipo VARCHAR(20),
                categoria VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
            );
        """))
        
        # Tabela de Grupos (Entidade independente do Muitos-para-Muitos)
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS grupo (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(50) NOT NULL
            );
        """))
        
        # Tabela Intermediária (Relacionamento Muitos-para-Muitos)
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS usuario_grupo (
                usuario_id INTEGER NOT NULL,
                grupo_id INTEGER NOT NULL,
                PRIMARY KEY (usuario_id, grupo_id),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
                FOREIGN KEY (grupo_id) REFERENCES grupo(id) ON DELETE CASCADE
            );
        """))
        
        db.session.commit()

def inserir_dados():
    db.session.execute(text("INSERT IGNORE INTO grupo (nome) VALUES ('Operação');"))
    db.session.execute(text("INSERT IGNORE INTO grupo (nome) VALUES ('Gerente');"))
    db.session.execute(text("INSERT IGNORE INTO grupo (nome) VALUES ('Cliente');"))
    db.session.execute(text("INSERT IGNORE INTO grupo (nome) VALUES ('Marketing');"))        
    db.session.execute(text("INSERT IGNORE INTO grupo (nome) VALUES ('Venda');"))        
    db.session.commit()