<h1 align="center">🥗 Daily Diet API</h1>

<p align="center">
  <strong>API RESTful para controle de dieta diária</strong> — desenvolvida com <a href="https://flask.palletsprojects.com/">Flask</a> como desafio prático da <a href="https://www.rocketseat.com.br/">Rocketseat</a>.  
  Permite o registro e gerenciamento de refeições, incluindo data, descrição e controle de dieta.
</p>

<p align="center">
  <a href="#-features-principais">✨ Features</a> •
  <a href="#-tech-stack">🚀 Tech Stack</a> •
  <a href="#-rodando-o-projeto-localmente">🏁 Rodando o Projeto</a> •
  <a href="#-endpoints-da-api">📡 Endpoints</a> •
  <a href="#-contexto">📄 Contexto</a>
</p>

---

## ✨ Features Principais

- ✅ **CRUD Completo:** Criação, leitura, atualização e exclusão de refeições.  
- 🧩 **Arquitetura Modular:** Estruturada com o padrão *Application Factory (`create_app`)*.  
- 🗂️ **Rotas Componentizadas:** Organização via *Blueprints* do Flask.  
- ⚙️ **Persistência de Dados:** Banco de dados **PostgreSQL (Neon)** com **Flask-SQLAlchemy**.  
- 🧱 **Migrações Automatizadas:** Gerenciadas com **Flask-Migrate (Alembic)**.  
- 🚫 **Tratamento Centralizado de Erros:** Respostas padronizadas em JSON.  
- 🔒 **Segurança:** Uso de variáveis de ambiente (`.env`) para dados sensíveis.  

---

## 🚀 Tech Stack

| Categoria | Tecnologias |
|------------|--------------|
| **Backend** | [Flask](https://flask.palletsprojects.com/) |
| **Banco de Dados** | [PostgreSQL (Neon)](https://neon.tech) |
| **ORM / Migrações** | Flask-SQLAlchemy, Flask-Migrate |
| **Drivers** | psycopg2-binary |
| **Ambiente** | python-dotenv, venv |

---

## 🏁 Rodando o Projeto Localmente

Siga os passos abaixo para executar o projeto em seu ambiente de desenvolvimento.  

### 🔧 Pré-requisitos

- 🐍 **Python 3.10+**
- 💾 **Git**
- 🗃️ **PostgreSQL** (crie gratuitamente no [Neon](https://neon.tech))

---

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/seu-usuario/daily-diet-api.git
cd daily-diet-api
````

---

### 2️⃣ Crie e Ative o Ambiente Virtual

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate

# Ativar no Windows
.\venv\Scripts\Activate.ps1
```

---

### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto (ele **não deve** ser versionado).

```bash
# macOS/Linux
touch .env

# Windows
echo. > .env
```

Adicione a sua URL de conexão do PostgreSQL:

```bash
DATABASE_URL='postgresql://usuario:senha@host.neon.tech/nome-do-banco'
```

---

### 5️⃣ Aplique as Migrações

```bash
# Define o app principal
export FLASK_APP=run.py
# No Windows: set FLASK_APP=run.py

# 1. Inicializa o diretório de migrações
flask db init

# 2. Gera o script de migração
flask db migrate -m "Initial migration. Create meal table."

# 3. Aplica no banco de dados
flask db upgrade
```

---

### 6️⃣ Inicie o Servidor

```bash
flask run
```

O servidor estará disponível em:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📡 Endpoints da API

> Todos os endpoints estão prefixados com `/api/v1`.

---

### 🔸 **POST /api/v1/meals**

Cria uma nova refeição.

#### Corpo da Requisição

```json
{
  "name": "Almoço",
  "description": "Frango grelhado e salada césar.",
  "meal_datetime": "2025-10-24T12:30:00",
  "is_on_diet": true
}
```

#### Resposta (201 Created)

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

---

### 🔸 **GET /api/v1/meals**

Lista todas as refeições.

#### Resposta (200 OK)

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

---

### 🔸 **GET /api/v1/meals/[int:meal_id](int:meal_id)**

Obtém os detalhes de uma refeição específica.

#### Resposta (200 OK)

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

#### Resposta (404 Not Found)

```json
{
  "message": "Refeição não encontrada."
}
```

---

### 🔸 **PUT /api/v1/meals/[int:meal_id](int:meal_id)**

Atualiza uma refeição existente.

#### Corpo da Requisição

```json
{
  "name": "Jantar Fora da Dieta",
  "description": "Pizza de calabresa",
  "meal_datetime": "2025-10-24T20:00:00",
  "is_on_diet": false
}
```

#### Resposta (200 OK)

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

---

### 🔸 **DELETE /api/v1/meals/[int:meal_id](int:meal_id)**

Remove uma refeição.

#### Resposta

```
Status Code: 204 No Content
Corpo: (vazio)
```

---

## 📄 Contexto

Este projeto foi desenvolvido como um **desafio avançado da Rocketseat**, com o objetivo de reforçar habilidades em:

* Flask e arquitetura modular;
* Criação de APIs RESTful completas;
* Boas práticas de versionamento e persistência de dados.

---

## 🧠 Autor

**Manoel Olímpio**
