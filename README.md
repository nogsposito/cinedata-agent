# CineData Analytics - Agente Text-to-SQL

Projeto desenvolvido para a atividade de GenAI do Rocket Lab 26.2.

O objetivo é permitir que usuários façam perguntas em linguagem natural sobre o catálogo de filmes da CineData Analytics, sem precisar escrever SQL manualmente.

## Tecnologias

- Python
- PydanticAI
- SQLite
- OpenRouter
- Streamlit

## Como funciona

```text
Pergunta em linguagem natural
        ↓
Agente PydanticAI
        ↓
Ferramentas de consulta
        ↓
Banco SQLite
        ↓
Resposta em linguagem natural + SQL utilizado
```

O agente possui ferramentas para:

- consultar o schema das tabelas;
- consultar valores distintos de colunas;
- executar consultas SQL.

Quando uma consulta retorna erro, o agente recebe a mensagem para tentar corrigir o SQL.

## Estrutura

```text
cinedata-agent/
├── .env.example
├── .gitignore
├── cinerocket.db
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    └── cinedata/
        ├── __init__.py
        ├── agent.py
        ├── app.py
        ├── config.py
        ├── database.py
        ├── evaluation.py
        ├── inspect_db.py
        ├── main.py
        └── models.py
```

O arquivo `.env` deve ser criado localmente e não deve ser enviado para o GitHub.

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```dotenv
OPENROUTER_API_KEY=sua_chave
MODEL_NAME=openrouter/free
```

Substitua `sua_chave` pela sua chave do OpenRouter.

Coloque também o arquivo `cinerocket.db` na raiz do projeto.

## Instalação

Na raiz do projeto, crie o ambiente virtual:

```powershell
python -m venv .venv
```

No PowerShell, ative com:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Prompt de Comando do Windows, ative com:

```bat
.venv\Scripts\activate.bat
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Executar pelo terminal

Na raiz do projeto:

```powershell
python -m src.cinedata.main
```

Exemplos de perguntas:

- Quais são os 5 filmes mais populares?
- Qual produtora possui o maior lucro total?
- Quais diretores possuem maior nota média IMDb considerando pelo menos 5 filmes?

## Interface com Streamlit

Para iniciar a interface, execute na raiz do projeto:

```powershell
python -m streamlit run src/cinedata/app.py
```

O Streamlit disponibiliza a aplicação no navegador.

Na interface, o usuário pode:

- escrever uma pergunta em linguagem natural;
- enviar a pergunta para o agente;
- visualizar a resposta;
- expandir a seção com o SQL utilizado.

## Segurança

A ferramenta de execução aceita consultas iniciadas por `SELECT` ou `WITH`.

A conexão abre o banco somente para leitura. O autorizador SQLite restringe as operações permitidas durante a execução das consultas.

Os nomes de tabelas e colunas usados pela ferramenta de valores distintos são validados contra o schema.

Os resultados das consultas são limitados a 100 linhas. Quando há mais resultados, a ferramenta informa o truncamento.

Consultas excessivamente caras podem ser interrompidas pelo limite de operações configurado.

## Avaliação

O projeto possui 14 perguntas em `src/cinedata/evaluation.py`, cobrindo:

- bilheteria e finanças;
- popularidade;
- elenco e equipe;
- gêneros e produtoras;
- avaliações dos usuários.

Para executar:

```powershell
python -m src.cinedata.evaluation
```

O script apresenta a resposta, o SQL e avisos sobre padrões esperados. Ao final, informa os casos sem avisos, os casos com avisos e os erros de execução.

Essa avaliação é heurística: verificar padrões no SQL não comprova a correção semântica dos resultados.

## Inspecionar o banco

Para visualizar tabelas, colunas, chaves estrangeiras e exemplos:

```powershell
python -m src.cinedata.inspect_db
```

## Observações

O agente utiliza `cinerocket.db` como fonte de dados.

O uso depende de uma chave válida, conexão com a internet e disponibilidade do modelo no OpenRouter.

A resposta estruturada contém os campos `answer` e `sql`. As instruções orientam o agente a informar o SQL realmente utilizado.