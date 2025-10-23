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

    # -----------------------------------------------------------------
    # REGISTRO DO BLUEPRINT (PASSO CHAVE)
    # -----------------------------------------------------------------
    # Importa o Blueprint que acabamos de criar
    from app.routes import bp as api_blueprint
    # Registra o Blueprint na nossa aplicação 'app'
    app.register_blueprint(api_blueprint)
    # -----------------------------------------------------------------

    return app