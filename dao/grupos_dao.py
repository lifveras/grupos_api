from sqlalchemy import text
from service import db

class GruposDAO:
    @staticmethod
    def busca_grupos(user_id):
        # Selecionar todos os grupos que o usuário está inserido
        query_grup = text("SELECT grupo_id FROM usuario_grupo WHERE usuario_id = :u_id")
        grupos = db.session.execute(query_grup, {"u_id": user_id}).scalars().all()
        return grupos
    