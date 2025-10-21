# config.py
import os

# Pega o caminho absoluto do diretório onde o arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Define a URI (o "endereço") do nosso banco de dados SQLite
    # Ele vai criar um arquivo 'app.db' na sua pasta principal
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Desativa uma funcionalidade do SQLAlchemy que não usaremos para evitar avisos
    SQLALCHEMY_TRACK_MODIFICATIONS = False