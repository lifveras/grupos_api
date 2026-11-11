from sqlalchemy import text
from service import db

class UsuarioDAO:    
    @staticmethod
    def salvar_usuario(dados):
        query_user = text("INSERT INTO usuario (nome, email, senha) VALUES (:nome, :email, :senha)")
        result = db.session.execute(query_user, {"nome": dados["nome"], "email": dados["email"], "senha": dados["senha"]})
        return result.lastrowid

    @staticmethod
    def adiciona_grupos(dados, usuario_id):
        # (MUITOS-PARA-MUITOS) Vincular o usuário com os grupos no banco: Relacionamento N:N
        query_grupo = text("INSERT INTO usuario_grupo (usuario_id, grupo_id) VALUES (:usuario_id, :grupo_id)")
        for grupo_id in dados["grupos_ids"]:
            db.session.execute(query_grupo, {"usuario_id": usuario_id, "grupo_id": grupo_id})
        db.session.commit()

    @staticmethod
    def buscar_todos():
        # Busca todos os usuários
        usuarios_rows = db.session.execute(text("SELECT id, nome, email FROM usuario")).mappings().all()
        return usuarios_rows

    @staticmethod
    def buscar_por_email(email):
        # Exemplo com SQL puro / Cursor que retorna dicionário/Row:
        sql = text("SELECT id, nome, email, senha FROM usuario WHERE email = :email")
        return db.session.execute(sql, {"email": email}).one_or_none()._mapping

