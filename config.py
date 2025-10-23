# config.py
import os
from dotenv import load_dotenv  # Importa a biblioteca

# Pega o caminho absoluto do diretório onde o arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega as variáveis do arquivo .env para o ambiente
# Isso faz com que os.environ.get('DATABASE_URL') funcione
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # Agora, lemos a string de conexão da variável de ambiente 'DATABASE_URL'.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Se DATABASE_URL não for encontrada, ele vai dar erro (o que é bom,
    # pois sabemos que precisamos dela).

    SQLALCHEMY_TRACK_MODIFICATIONS = False