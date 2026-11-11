from flask import Flask, request, jsonify
from flask_cors import CORS
from service import bcrypt, flask_jwt, db, criar_tabelas, inserir_dados
from repository.usuario_repository import UsuarioRepository
import os
from dotenv import load_dotenv
from routes.usuario_route import usuario_blueprint
from routes.auth_route import auth_blueprint

# Carrega as variáveis de ambiente
load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD") # Recupera a senha do banco de dados
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") 

app = Flask(__name__)

app.register_blueprint(usuario_blueprint)
app.register_blueprint(auth_blueprint)

CORS(app, resources={
    r"/usuario*": {"origins": "*"},
    r"/login*": {"origins": "*"}
})

# Define variáveis do Flask
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://avnadmin:{DB_PASSWORD}@braltp3-db-braltp3.h.aivencloud.com:28010/grupos_db"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {} # Um dicionário vazio força o PyMySQL a utilizar uma conexão SSL padrão
    }
}

# Associa extensões ao Flask
jwt = flask_jwt.init_app(app)
bcrypt = bcrypt.init_app(app)
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        criar_tabelas()
        inserir_dados()

    app.run(debug=True)