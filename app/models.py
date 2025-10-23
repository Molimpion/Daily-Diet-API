# app/models.py
from app import db
from datetime import datetime

class Meal(db.Model):
    """
    Representa uma refeição registrada no banco de dados.
    Esta classe define o esquema da tabela 'meal'.
    """
    
    # Define o nome da tabela no banco (boa prática, embora opcional)
    __tablename__ = 'meal'

    # -----------------------------------------------------------------
    # Colunas da Tabela
    # -----------------------------------------------------------------
    
    # Chave primária: Identificador único para cada refeição.
    id = db.Column(db.Integer, primary_key=True)
    
    # Nome da refeição (ex: "Almoço", "Lanche da Tarde")
    # nullable=False: Este campo não pode ser nulo (obrigatório).
    name = db.Column(db.String(100), nullable=False)
    
    # Descrição do que foi comido.
    # nullable=True: Este campo pode ser nulo (opcional).
    description = db.Column(db.String(255), nullable=True)
    
    # Data e hora em que a refeição ocorreu, informada pelo usuário.
    # nullable=False: O usuário deve informar quando comeu.
    meal_datetime = db.Column(db.DateTime, nullable=False)
    
    # Booleano que indica se a refeição estava dentro da dieta.
    # default=False: Uma boa prática é definir um padrão seguro.
    is_on_diet = db.Column(db.Boolean, nullable=False, default=False)
    
    
    # -----------------------------------------------------------------
    # Prática Sênior: Colunas de Auditoria (Timestamps)
    # -----------------------------------------------------------------
    
    # Timestamp de quando o registro foi criado.
    # default=datetime.utcnow: Define o valor padrão para a data/hora
    #                          atual em UTC no momento da criação.
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Timestamp de quando o registro foi atualizado pela última vez.
    # onupdate=datetime.utcnow: Atualiza automaticamente este campo
    #                           com a data/hora UTC sempre que o
    #                           registro for modificado.
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


    # -----------------------------------------------------------------
    # Prática Sênior: Método de Representação (Debuggabilidade)
    # -----------------------------------------------------------------
    def __repr__(self):
        """
        Retorna uma representação em string legível do objeto Meal,
        útil para debugging.
        """
        return f'<Meal {self.id}: {self.name} (On Diet: {self.is_on_diet})>'


    # -----------------------------------------------------------------
    # Prática Sênior: Método de Serialização (Princípio DRY)
    # -----------------------------------------------------------------
    def to_dict(self):
        """
        Converte o objeto Meal em um dicionário serializável para
        respostas de API (JSON).
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            # .isoformat(): Converte o objeto datetime em uma string
            #                no padrão ISO 8601, que é o padrão para JSON.
            'meal_datetime': self.meal_datetime.isoformat(),
            'is_on_diet': self.is_on_diet,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }