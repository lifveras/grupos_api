from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from repository.usuario_repository import UsuarioRepository
from service import bcrypt

auth_blueprint = Blueprint("auth_route", __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    
    # Validação dos campos recebidos
    if not dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    # Busca o usuário pelo e-mail
    usuario = UsuarioRepository.buscar_por_email(dados['email'])

    # Valida se o usuário existe e se a senha bate com o hash salvo
    if not usuario or not bcrypt.check_password_hash(usuario["senha"], dados['senha']):
        # Dica de segurança: Retorne a mesma mensagem genérica para e-mail incorreto ou senha incorreta
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    # Gera o Token JWT com a identidade do usuário (ID)
    access_token = create_access_token(identity=str(usuario["id"]))

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "access_token": access_token
    }), 200