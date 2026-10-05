# CineData Analytics - Agente Text-to-SQL

Projeto desenvolvido para a atividade de GenAI do Rocket Lab 26.2.

O objetivo é permitir que usuários façam perguntas em linguagem natural sobre o catálogo de filmes da CineData Analytics, sem precisar escrever SQL manualmente.

## Tecnologias

- Python
- PydanticAI
- SQLite
- OpenRouter

## Como funciona

O fluxo principal é:

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
- executar consultas SQL;
- corrigir consultas quando ocorre erro.

## Estrutura

```text
src/
└── cinedata/
    ├── agent.py
    ├── config.py
    ├── database.py
    ├── evaluation.py
    ├── main.py
    └── models.py
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENROUTER_API_KEY=sua_chave
MODEL_NAME=openrouter/free
```

O arquivo `.env` não deve ser enviado para o GitHub.

Coloque também o arquivo `cinerocket.db` na raiz do projeto.

## Instalação

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows, ative com:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar

Na raiz do projeto:

```bash
python -m src.cinedata.main
```

Exemplos de perguntas:

```text
Quais são os 5 filmes mais populares?
```

```text
Qual produtora possui o maior lucro total?
```

```text
Quais diretores possuem maior nota média IMDb considerando pelo menos 5 filmes?
```

## Segurança

O agente permite apenas consultas SQL de leitura.

São aceitas consultas iniciadas por:

```sql
SELECT
WITH
```

Comandos de alteração do banco são bloqueados, como:

```sql
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
```

## Avaliação

O projeto possui um conjunto de perguntas em:

```text
src/cinedata/evaluation.py
```

As perguntas cobrem categorias como:

- bilheteria e finanças;
- popularidade;
- elenco e equipe;
- gêneros e produtoras;
- avaliações dos usuários.

Para executar:

```bash
python -m src.cinedata.evaluation
```

## Interface com Streamlit

Além da execução pelo terminal, o projeto possui uma interface simples em Streamlit para facilitar o uso do agente.

Para iniciar a interface, execute na raiz do projeto:

```bash
python -m streamlit run src/cinedata/app.py

## Observações

O agente utiliza o banco `cinerocket.db` como fonte de dados e retorna também a consulta SQL utilizada para gerar cada resposta.
