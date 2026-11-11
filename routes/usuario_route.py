from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
usuario_blueprint = Blueprint("usuario_route", __name__)
from repository.usuario_repository import UsuarioRepository
from service import db

@usuario_blueprint.route('/usuario', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    # Validação simples dos campos obrigatórios
    if not dados or "nome" not in dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    try:
        usuario_id = UsuarioRepository.salvar_usuario(dados)
        return jsonify({"mensagem": "Usuário criado com sucesso", "id": usuario_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Falha ao salvar dados: {str(e)}"}), 500

@usuario_blueprint.route('/usuario', methods=['GET'])
@jwt_required()
def listar_usuarios():
    try:
        usuarios = UsuarioRepository.buscar_todos_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": f"Falha ao buscar dados: {str(e)}"}), 500