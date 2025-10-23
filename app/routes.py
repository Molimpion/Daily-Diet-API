# app/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Meal
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError # Prática Sênior: Importa o erro específico do DB

# Prática Sênior: Importa nosso erro personalizado
from app.errors import InvalidAPIUsage 

bp = Blueprint('api', __name__, url_prefix='/api/v1')

# -----------------------------------------------------------------
# Prática Sênior: Manipulador de Erro CENTRALIZADO
# -----------------------------------------------------------------
# Este decorador diz ao Blueprint: "Quando uma exceção do tipo
# 'InvalidAPIUsage' for levantada em qualquer rota deste blueprint,
# execute esta função."
@bp.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    """
    Captura nossa exceção personalizada e retorna uma resposta
    JSON formatada e padronizada.
    """
    # Usamos o método .to_dict() que criamos na nossa classe de erro
    response = jsonify(error.to_dict())
    # Definimos o status code da resposta com base no erro
    response.status_code = error.status_code
    return response

# -----------------------------------------------------------------
# Endpoint: Criar uma Nova Refeição (Create)
# (Refatorado para usar 'raise')
# -----------------------------------------------------------------
@bp.route('/meals', methods=['POST'])
def create_meal():
    """
    Cria um novo registro de refeição com base nos dados JSON 
    fornecidos no corpo da requisição.
    """
    data = request.get_json()

    # 1. Validação de Entrada (agora usando 'raise')
    if not data:
        # Em vez de 'return jsonify...', nós "levantamos" nosso erro.
        # O manipulador @bp.errorhandler(InvalidAPIUsage) vai pegá-lo.
        raise InvalidAPIUsage('Corpo da requisição não pode ser vazio.', status_code=400)

    required_fields = ['name', 'meal_datetime', 'is_on_diet']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        # Levantamos o erro com uma mensagem clara.
        raise InvalidAPIUsage(f'Campos obrigatórios ausentes: {", ".join(missing_fields)}', status_code=400)
    
    # 2. Tratamento e Conversão de Tipos (agora usando 'raise')
    try:
        meal_datetime_obj = datetime.fromisoformat(data['meal_datetime'])
    except (ValueError, TypeError):
        raise InvalidAPIUsage('Formato de "meal_datetime" inválido. Use o padrão ISO 8601 (YYYY-MM-DDTHH:MM:SS).', status_code=400)

    # 3. Criação da Instância do Modelo
    new_meal = Meal(
        name=data['name'],
        description=data.get('description'), 
        meal_datetime=meal_datetime_obj,
        is_on_diet=bool(data['is_on_diet'])
    )

    # 4. Persistência no Banco de Dados (agora com try/except específico)
    try:
        db.session.add(new_meal)
        db.session.commit()
    
    # Prática Sênior: NUNCA use 'except Exception'.
    # Capture apenas as exceções que você espera.
    # 'SQLAlchemyError' é a classe base para todos os erros do SQLAlchemy.
    except SQLAlchemyError as e:
        db.session.rollback()
        # Levantamos um erro 500 (Erro Interno do Servidor)
        # O 'str(e)' dá detalhes sobre o erro do banco no log,
        # mas retornamos uma mensagem genérica para o usuário.
        print(f"Erro de banco de dados: {str(e)}") # Log para o dev
        raise InvalidAPIUsage("Erro interno ao salvar os dados.", status_code=500)

    # 5. Resposta de Sucesso
    return jsonify({
        'message': 'Refeição criada com sucesso!',
        'meal': new_meal.to_dict()
    }), 201