# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializa as extensões, mas sem associá-las a uma aplicação ainda
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Cria a instância da aplicação Flask
    app = Flask(__name__)
    # Carrega as configurações do nosso arquivo config.py
    app.config.from_object(config_class)

    # Associa as extensões à instância da aplicação
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa e registra o Blueprint com as rotas (faremos em breve)
    # Por enquanto, vamos deixar comentado para não dar erro
    # from app.routes import bp as main_bp
    # app.register_blueprint(main_bp)

    return app