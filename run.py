# run.py
from app import create_app, db
from app.models import Meal

# 1. Criação da Aplicação
# -----------------------------------------------------------------
# Chamamos nossa factory 'create_app' que está no app/__init__.py
# A factory carrega a configuração, inicializa o db e os blueprints.
app = create_app()

# 2. Configuração do Contexto do Shell (Prática Sênior)
# -----------------------------------------------------------------
# Esta função é um "decorador" do Flask. Ela registra a função
# 'make_shell_context' para ser executada quando o comando
# 'flask shell' for utilizado.
@app.shell_context_processor
def make_shell_context():
    """
    Configura o shell interativo do Flask ('flask shell')
    para pré-importar itens úteis para depuração.
    
    Isso nos poupa de ter que digitar 'from app import db' ou
    'from app.models import Meal' toda vez que abrimos o shell.
    """
    return {
        'db': db,
        'Meal': Meal
    }

# 3. Ponto de Execução (Opcional, mas bom para clareza)
# -----------------------------------------------------------------
# Este bloco 'if' permite rodar a aplicação diretamente com
# 'python run.py', que é uma alternativa a 'flask run'.
# 'flask run' é o método preferido, mas isso não prejudica.
if __name__ == '__main__':
    app.run()