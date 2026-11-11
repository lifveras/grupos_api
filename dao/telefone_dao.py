from sqlalchemy import text
from service import db

class TelefoneDAO:    
    @staticmethod
    def busca_telefones(user_id):
        query_tel = text("SELECT ddd, numero, tipo, categoria FROM telefone WHERE usuario_id = :u_id")
        telefones = db.session.execute(query_tel, {"u_id": user_id}).mappings().all()
        return telefones

    @staticmethod
    def salva_telefones(dados, usuario_id):
        #(UM-PARA-MUITOS) Insere os Telefones de um usuário
        query_tel = text("""
                INSERT INTO telefone (usuario_id, ddd, numero, tipo, categoria) 
                VALUES (:usuario_id, :ddd, :numero, :tipo, :categoria)
            """)
        for tel in dados["telefones"]:
            db.session.execute(query_tel, {
                    "usuario_id": usuario_id,
                    "ddd": tel.get("ddd"),
                    "numero": tel.get("numero"),
                    "tipo": tel.get("tipo"),
                    "categoria": tel.get("categoria")
                })