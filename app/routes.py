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

    # -----------------------------------------------------------------
# Endpoint: Listar Todas as Refeições (Read - All)
# -----------------------------------------------------------------
# Rota: GET /api/v1/meals
# -----------------------------------------------------------------
@bp.route('/meals', methods=['GET'])
def get_meals():
    """
    Retorna uma lista de todas as refeições registradas.
    """
    try:
        # 1. Consulta o banco de dados
        # Prática Sênior: Usamos .order_by() para garantir uma
        # ordem consistente, o que é bom para paginação no futuro.
        # Aqui, ordenamos pela data da refeição, da mais recente para a mais antiga.
        all_meals = Meal.query.order_by(Meal.meal_datetime.desc()).all()
        
        # 2. Serialização
        # Prática Sênior: Usamos uma "List Comprehension" para aplicar
        # nosso método .to_dict() em cada objeto 'meal' na lista.
        # Isso é limpo e muito eficiente em Python.
        meals_list = [meal.to_dict() for meal in all_meals]
        
        # 3. Resposta
        return jsonify({'meals': meals_list}), 200

    except SQLAlchemyError as e:
        # Se a consulta ao banco falhar por algum motivo.
        print(f"Erro de banco de dados: {str(e)}")
        raise InvalidAPIUsage("Erro interno ao consultar o banco de dados.", status_code=500)

# -----------------------------------------------------------------
# Endpoint: Obter Uma Refeição Específica (Read - One)
# -----------------------------------------------------------------
# Rota: GET /api/v1/meals/<int:meal_id>
# <int:meal_id>: Isso é um "conversor de rota". O Flask captura
# o valor da URL (ex: /meals/1), garante que é um inteiro,
# e o passa como um argumento chamado 'meal_id' para nossa função.
# -----------------------------------------------------------------
@bp.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    """
    Retorna os detalhes de uma refeição específica pelo seu ID.
    """
    try:
        # 1. Consulta o banco de dados
        # .get() é a forma mais simples de buscar por chave primária (ID).
        meal = Meal.query.get(meal_id)
        
        # 2. Prática Sênior: Tratamento de "Não Encontrado"
        # Verificamos se 'meal' é None (não encontrado).
        if not meal:
            # Em vez de deixar o Flask retornar um 404 de HTML genérico,
            # nós levantamos nosso erro personalizado. Isso garante que
            # o cliente da API receberá um JSON padronizado.
            raise InvalidAPIUsage("Refeição não encontrada.", status_code=404)
            
        # 3. Serialização e Resposta
        # Se encontramos a refeição, retornamos seu .to_dict().
        return jsonify({'meal': meal.to_dict()}), 200

    except SQLAlchemyError as e:
        print(f"Erro de banco de dados: {str(e)}")
        raise InvalidAPIUsage("Erro interno ao consultar o banco de dados.", status_code=500)


# Endpoint: Atualizar uma Refeição (Update)
# -----------------------------------------------------------------
# Rota: PUT /api/v1/meals/<int:meal_id>
# Usamos PUT para a substituição completa do recurso.
# -----------------------------------------------------------------
@bp.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    """
    Atualiza (substitui) uma refeição existente com base no seu ID.
    O corpo da requisição deve conter o objeto *completo* da refeição.
    """
    try:
        # 1. Encontrar o Recurso
        # Primeiro, buscamos a refeição no banco.
        meal_to_update = Meal.query.get(meal_id)
        
        # 2. Tratar "Não Encontrado" (mesma lógica do get_meal)
        if not meal_to_update:
            raise InvalidAPIUsage("Refeição não encontrada.", status_code=404)
            
        # 3. Obter e Validar os Dados de Entrada
        data = request.get_json()
        if not data:
            raise InvalidAPIUsage('Corpo da requisição não pode ser vazio.', status_code=400)

        required_fields = ['name', 'meal_datetime', 'is_on_diet']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise InvalidAPIUsage(f'Campos obrigatórios ausentes: {", ".join(missing_fields)}', status_code=400)
        
        # 4. Validar o Formato da Data (mesma lógica do create_meal)
        try:
            meal_datetime_obj = datetime.fromisoformat(data['meal_datetime'])
        except (ValueError, TypeError):
            raise InvalidAPIUsage('Formato de "meal_datetime" inválido. Use o padrão ISO 8601 (YYYY-MM-DDTHH:MM:SS).', status_code=400)
            
        # 5. Atualizar os Campos do Objeto
        # Prática Sênior: Atualizamos o objeto que já foi
        # carregado da sessão do SQLAlchemy.
        meal_to_update.name = data['name']
        meal_to_update.description = data.get('description') # Opcional
        meal_to_update.meal_datetime = meal_datetime_obj
        meal_to_update.is_on_diet = bool(data['is_on_diet'])
        
        # Nota: O campo 'updated_at' será atualizado automaticamente
        # graças ao 'onupdate=datetime.utcnow' que definimos no modelo.

        # 6. Persistir as Mudanças
        # Como o objeto 'meal_to_update' já estava na sessão
        # (desde o .get(meal_id)), só precisamos dar 'commit'.
        db.session.commit()
        
        # 7. Retornar o Recurso Atualizado
        return jsonify({
            'message': 'Refeição atualizada com sucesso!',
            'meal': meal_to_update.to_dict()
        }), 200 # 200 OK é o status padrão para um PUT bem-sucedido

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Erro de banco de dados: {str(e)}")
        raise InvalidAPIUsage("Erro interno ao atualizar os dados.", status_code=500)