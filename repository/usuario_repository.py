from dao.usuario_dao import UsuarioDAO
from dao.telefone_dao import TelefoneDAO
from dao.grupos_dao import GruposDAO
from service import bcrypt

class UsuarioRepository:
    @staticmethod
    def salvar_usuario(dados):
        senha_hash = bcrypt.generate_password_hash(dados['senha']).decode('utf-8')
        dados["senha"] = senha_hash
        
        usuario_id = UsuarioDAO.salvar_usuario(dados)
        
        # (UM-PARA-MUITOS) Insere os Telefones
        if "telefones" in dados:
            TelefoneDAO.salva_telefones(dados, usuario_id)

        # (MUITOS-PARA-MUITOS) Associa os grupos ao usuário no Banco
        if "grupos_ids" in dados:
            UsuarioDAO.adiciona_grupos(dados, usuario_id)
                
        return usuario_id
    
    @staticmethod
    def buscar_todos_usuarios():
        usuarios_rows = UsuarioDAO.buscar_todos()
        resultado = []
        
        for user in usuarios_rows:
            user_id = user["id"]
            
            # Busca os telefones do usuário atual
            telefones = TelefoneDAO.busca_telefones(user_id)
            
            # Busca os IDs dos grupos vinculados (Muitos-para-Muitos)
            grupos = GruposDAO.busca_grupos(user_id)
            
            # Monta o nó estruturado no formato JSON desejado
            resultado.append({
                "id": user_id,
                "nome": user["nome"],
                "email": user["email"],
                "telefones": [dict(t) for t in telefones],
                "grupos_ids": list(grupos)
            })
            
        return resultado

    @staticmethod
    def buscar_por_email(email):
        user = UsuarioDAO.buscar_por_email(email)
        if not user:
            return None
        print(user)
        user_id = user["id"]
        telefones = TelefoneDAO.busca_telefones(user_id)
        grupos = GruposDAO.busca_grupos(user_id)

        return {
            "id": user_id,
            "nome": user["nome"],
            "email": user["email"],
            "senha": user["senha"],  # Incluído para permitir a validação do hash no login
            "telefones": [dict(t) for t in telefones],
            "grupos_ids": list(grupos)
        }
