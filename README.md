# Daily Diet API

Esta é uma API RESTful completa para o controle de dieta diária, desenvolvida como um desafio prático de Flask. A aplicação permite o registro e gerenciamento de refeições, com informações detalhadas como nome, descrição, data/hora e se a refeição está ou não dentro da dieta.

O objetivo deste projeto foi reforçar conceitos avançados de Flask e o desenvolvimento de APIs RESTful, implementando funcionalidades completas de CRUD (Criar, Ler, Atualizar, Deletar) com persistência em banco de dados.

## Features Principais

* **Gerenciamento de Refeições:** Sistema completo de CRUD (Criar, Ler, Atualizar, Deletar) para o gerenciamento de refeições.
* **Persistência de Dados:** Utiliza PostgreSQL (hospedado na Neon) como banco de dados, com o ORM Flask-SQLAlchemy e gerenciamento de migrações com Flask-Migrate.
* **Arquitetura Avançada:** Construído usando o padrão Application Factory (`create_app`) para modularidade e testabilidade.
* **Rotas Componentizadas:** Utiliza Blueprints do Flask para agrupar e organizar os endpoints da API.
* **Tratamento de Erros:** Implementa um sistema de tratamento de erros personalizado e centralizado, que retorna respostas JSON padronizadas para a API.
* **Configuração Segura:** Gerenciamento de 'secrets' (como a URL do banco de dados) de forma segura através de variáveis de ambiente (`.env`).

## Tech Stack (Tecnologias Usadas)

* **Backend:** Flask
* **Banco de Dados:** PostgreSQL (hospedado na Neon)
* **ORM e Migrações:** Flask-SQLAlchemy, Flask-Migrate (Alembic)
* **Drivers:** psycopg2-binary
* **Ambiente:** python-dotenv, venv

## Rodando o Projeto Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente de desenvolvimento.

### Pré-requisitos

* Python 3.10+
* Git
* Um banco de dados PostgreSQL. Você pode criar uma conta gratuita no [Neon](https://neon.tech/) para obter uma URL de conexão em 1 minuto.

### 1. Clone o Repositório

```bash
git clone [https://github.com/seu-usuario/daily-diet-api.git](https://github.com/seu-usuario/daily-diet-api.git)
cd daily-diet-api
````

### 2\. Crie e Ative o Ambiente Virtual (venv)

```bash
# Criar o ambiente
python -m venv venv

# Ativar no macOS/Linux (Bash)
source venv/bin/activate

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3\. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4\. Configure as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto. Este arquivo não deve ser enviado ao Git.

```bash
# Crie o arquivo (macOS/Linux)
touch .env

# Crie o arquivo (Windows)
echo. > .env
```

Abra o arquivo `.env` e adicione a sua string de conexão do PostgreSQL (copiada do Neon ou do seu banco local):

```ini
# .env
DATABASE_URL='postgresql://usuario:senha@host.neon.tech/nome-do-banco'
```

### 5\. Aplique as Migrações do Banco

Esses comandos irão criar as tabelas no seu banco de dados com base nos modelos definidos em `app/models.py`.

```bash
# Define o app principal para o Flask (macOS/Linux)
export FLASK_APP=run.py
# No Windows: set FLASK_APP=run.py

# 1. Inicializa a pasta 'migrations' (só na primeira vez)
flask db init

# 2. Gera o script de migração
flask db migrate -m "Initial migration. Create meal table."

# 3. Aplica o script no banco de dados
flask db upgrade
```

### 6\. Inicie o Servidor

```bash
flask run
```

O servidor estará rodando em `http://127.0.0.1:5000`.

## Endpoints da API (Uso)

Todos os endpoints estão prefixados com `/api/v1`.

### `POST /api/v1/meals`

Cria um novo registro de refeição.

**Corpo da Requisição (JSON):**

```json
{
  "name": "Almoço",
  "description": "Frango grelhado e salada césar.",
  "meal_datetime": "2025-10-24T12:30:00",
  "is_on_diet": true
}
```

**Resposta de Sucesso (201 Created):**

```json
{
  "message": "Refeição criada com sucesso!",
  "meal": {
    "id": 1,
    "name": "Almoço",
    "description": "Frango grelhado e salada césar.",
    "meal_datetime": "2025-10-24T12:30:00",
    "is_on_diet": true,
    "created_at": "2025-10-24T10:00:00.123456",
    "updated_at": "2025-10-24T10:00:00.123456"
  }
}
```

### `GET /api/v1/meals`

Retorna uma lista de todas as refeições registradas.

**Resposta de Sucesso (200 OK):**

```json
{
  "meals": [
    {
      "id": 1,
      "name": "Almoço",
      "description": "Frango grelhado e salada césar.",
      "meal_datetime": "2025-10-24T12:30:00",
      "is_on_diet": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### `GET /api/v1/meals/<int:meal_id>`

Retorna os detalhes de uma refeição específica.

**Resposta de Sucesso (200 OK):**

```json
{
  "meal": {
    "id": 1,
    "name": "Almoço",
    "description": "Frango grelhado e salada césar.",
    "meal_datetime": "2025-10-24T12:30:00",
    "is_on_diet": true,
    "created_at": "2025-10-24T10:00:00.123456",
    "updated_at": "2025-10-24T10:00:00.123456"
  }
}
```

**Resposta de Erro (404 Not Found):**

```json
{
  "message": "Refeição não encontrada."
}
```

### `PUT /api/v1/meals/<int:meal_id>`

Atualiza (substitui) uma refeição existente. O corpo da requisição deve ser o objeto completo.

**Corpo da Requisição (JSON):**

```json
{
  "name": "Jantar Fora da Dieta",
  "description": "Pizza de calabresa",
  "meal_datetime": "2025-10-24T20:00:00",
  "is_on_diet": false
}
```

**Resposta de Sucesso (200 OK):**

```json
{
  "message": "Refeição atualizada com sucesso!",
  "meal": {
    "id": 1,
    "name": "Jantar Fora da Dieta",
    "description": "Pizza de calabresa",
    "meal_datetime": "2025-10-24T20:00:00",
    "is_on_diet": false,
    "created_at": "2025-10-24T10:00:00.123456",
    "updated_at": "2025-10-24T11:30:00.654321"
  }
}
```

### `DELETE /api/v1/meals/<int:meal_id>`

Deleta uma refeição específica do banco de dados.

**Resposta de Sucesso:**

  * **Status Code:** `204 No Content`
  * **Corpo da Resposta:** Vazio.

-----

## Origem do Projeto

Este projeto foi desenvolvido como um desafio avançado proposto pela Rocketseat.
