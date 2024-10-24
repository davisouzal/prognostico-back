# API de Prognóstico 

API da aplicação de prognóstico de doenças hepáticas desenvolvida para a matéria de Gerência de Projeto.

## Requisitos

-   **Python 3.8 ou superior**
-   **Flask**

## Instruções para Instalação

### 1. Clone o repositório
`git clone https://github.com/seu-usuario/projeto-flask-prognostico.git`
`cd projeto-flask-prognostico` 

### 2. Crie um ambiente virtual (recomendado)

#### No Windows:

`python -m venv venv`
`venv\Scripts\activate` 

#### No Linux:

`python3 -m venv venv`
`source venv/bin/activate` 

### 3. Instale as dependências

Com o ambiente virtual ativado, execute:

`pip install -r requirements.txt` 

> Nota: Certifique-se de que o arquivo `requirements.txt` contenha as bibliotecas necessárias, como Flask e outras.

## Executando a aplicação

Após instalar as dependências, você pode iniciar a aplicação localmente.

#### No Windows:

`set FLASK_APP=app`
`set FLASK_ENV=development`
`flask run`

#### No Linux:
`export FLASK_APP=app`
`export FLASK_ENV=development`
`flask run` 

>Obs: Tabém pode rodar no modo debug:  `flask --app app --debug run`

Isso iniciará o servidor Flask em modo de desenvolvimento na porta `5000`. Acesse a aplicação via navegador no endereço `http://127.0.0.1:5000`.

# Rotas da API

## 1. Obter Todos os Usuários
 - Rota: /users
 - Método: GET
 - Descrição: Retorna uma lista de todos os usuários cadastrados, incluindo seus dados patológicos e prognósticos.
 - Exemplo de Resposta:
 ```
[
  {
    "id": 1,
    "cpf": "123456789",
    "name": "John Doe",
    "email": "john@example.com",
    "birthDate": "1980-01-01",
    "gender": "M",
    "status": true,
    "type": "admin",
    "pathological_data": [
      {
        "diff_diag": "Condition A",
        "encephalopathy": "None",
        "ascites": "Mild",
        "inr": 1.2,
        "total_bilirubin": 1.5,
        "albumin": 3.4
      }
    ],
    "prognosis": [
      {
        "class": "A",
        "score": 5,
        "one_year": 95.0,
        "two_years": 90.0,
        "perioperative_mortality": "Low",
        "comments": "Stable"
      }
    ]
  }
] 
```

## 2. Obter Usuário por ID
 - Rota: /user/<int:user_id>
 - Método: GET
 - Descrição: Retorna os dados de um usuário específico pelo seu ID, incluindo dados patológicos e prognósticos.
 - Exemplo de Resposta:

```
{
  "id": 1,
  "cpf": "123456789",
  "name": "John Doe",
  "email": "john@example.com",
  "birthDate": "1980-01-01",
  "gender": "M",
  "status": true,
  "type": "admin",
  "pathological_data": [
    {
      "diff_diag": "Condition A",
      "encephalopathy": "None",
      "ascites": "Mild",
      "inr": 1.2,
      "total_bilirubin": 1.5,
      "albumin": 3.4
    }
  ],
  "prognosis": [
    {
      "class": "A",
      "score": 5,
      "one_year": 95.0,
      "two_years": 90.0,
      "perioperative_mortality": "Low",
      "comments": "Stable"
    }
  ]
}
```

## 4. Criar Usuário e Dados Patológicos
 - Rota: /user
 - Método: POST
 - Descrição: Cria um novo usuário com seus dados patológicos.
- Exemplo de Payload (JSON):

```
{
  "cpf": "123456789",
  "name": "John Doe",
  "email": "john@example.com",
  "birthDate": "1980-01-01",
  "gender": "M",
  "status": true,
  "password": "password123",
  "type": "admin",
  "pathological_data": {
    "diff_diag": "Condition A",
    "encephalopathy": "None",
    "ascites": "Mild",
    "inr": 1.2,
    "total_bilirubin": 1.5,
    "albumin": 3.4
  }
}
Exemplo de Resposta:
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "cpf": "123456789",
    "name": "John Doe",
    "email": "john@example.com",
    "birthDate": "1980-01-01",
    "gender": "M",
    "status": true,
    "type": "admin"
  }
}
```