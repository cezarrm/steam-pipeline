# Steam Analytics Dashboard
![Demo do Dashboard](img/dashboard_view.gif)

Projeto de Engenharia de Dados para análise de jogos da Steam,
utilizando pipeline em Python, MySQL, Docker e Metabase para
visualização interativa.

------------------------------------------------------------------------

## Arquitetura do Projeto

Pipeline completo:

API / Fonte de Dados\
↓\
Python (ETL)\
↓\
MySQL (Armazenamento + Views Analíticas)\
↓\
Metabase (Dashboard Interativo)

------------------------------------------------------------------------

## Tecnologias Utilizadas

-   Python
-   MySQL 8
-   Docker & Docker Compose
-   Metabase
-   SQL (Views analíticas)

------------------------------------------------------------------------

## Estrutura do Projeto
```text
STEAM-PIPELINE/
├── data/
│   └─ processed/               # Armazenamento do CSV processado e enriquecido.
│   └─ raw/                     # Armazenamento do CSV extraido da API.
├── extract/
│   └─ steam_api.py/            # Função de extração dos dados da API.
│
├── img/
│   └─ dashboard_view.py/       # Demonstração do dashboard
│  
├── load/
│   └─ create_views.py/         # Cria as view dentro do MySQL
│   └─ load_games.py            # Carrega os dados no MySQL
│  
├── transform/
│   └─ enrich_data.py           # Enriquecimento dos dados usando API de terceiro (captura dos gêneros dos jogos).
│   └─ transform_games.py       # Normalização dos dados
|
├── docker-compose.yml          # Orquestração Docker
├── dockerfile                  # Containerização
├── main.py                     # Orquestração da aplicação
├── requirements.txt            # Dependências Python
├── .env                        # Credenciais
├── README.md
```
------------------------------------------------------------------------

## Execução com Docker

Subir o ambiente:
```bash
docker compose up --build
```
Parar containers:
```bash
docker compose down
```

Atenção: Não utilizar -v caso queira manter os dados persistidos.

------------------------------------------------------------------------

## Banco de Dados

Banco principal:

- steam_db

Banco de metadata do Metabase:

- metabase

------------------------------------------------------------------------

## Views Criadas

Algumas perguntas foram ajustadas dentro do metabase para melhor análise.
### 🔹 1. Total Geral de Horas

#### vw_total_playtime
```bash
    SELECT SUM(playtime_hours) AS total_hours
    FROM games;
```
Responsável por calcular o total geral de horas jogadas (KPI principal).

------------------------------------------------------------------------

### 🔹 2. Estatísticas Gerais

#### vw_overview_stats
```bash
    SELECT 
        COUNT(*) AS total_games,
        SUM(playtime_hours) AS total_hours,
        AVG(playtime_hours) AS avg_hours_per_game
    FROM games;
```
Inclui:

-   Total de jogos
-   Total de horas
-   Média de horas por jogo

------------------------------------------------------------------------

### 🔹 3. Normalização de Gêneros

vw_game_genres
```bash
    SELECT 
        game_name,
        TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(genres, ',', numbers.n), ',', -1)) AS genre
    FROM games
    JOIN numbers ON CHAR_LENGTH(genres) 
        - CHAR_LENGTH(REPLACE(genres, ',', '')) >= numbers.n - 1;
```

Explode múltiplos gêneros em linhas separadas, permitindo análise
correta em BI.

------------------------------------------------------------------------

### 🔹 4. Quantidade de Jogos por Gênero

vw_games_count_by_genre
```bash
    SELECT 
        genre,
        COUNT(*) AS total_games
    FROM vw_game_genres
    GROUP BY genre
    ORDER BY total_games DESC;

```
Mostra o total de jogos por gênero.

------------------------------------------------------------------------

### 🔹 5. Total de Horas por Gênero

vw_playtime_by_genre
```bash
    SELECT 
        g.genre,
        SUM(gm.playtime_hours) AS total_hours
    FROM vw_game_genres g
    JOIN games gm ON g.game_name = gm.game_name
    GROUP BY g.genre
    ORDER BY total_hours DESC;

```
Permite identificar quais gêneros possuem maior engajamento.

------------------------------------------------------------------------


### 🔹 6. Distribuição por Faixa por Gênero

vw_playtime_distribution_by_genre
```bash
    SELECT
        genre,
        CASE 
            WHEN playtime_hours <= 10 THEN '0–10h'
            WHEN playtime_hours <= 50 THEN '10–50h'
            WHEN playtime_hours <= 100 THEN '50–100h'
            ELSE '100h+'
        END AS playtime_range,
        COUNT(*) AS total_games
    FROM vw_game_genres g
    JOIN games gm ON g.game_name = gm.game_name
    GROUP BY genre, playtime_range;

```
Análise cruzada entre:

-   Gênero
-   Faixa de tempo
-   Quantidade de jogos

------------------------------------------------------------------------

## Dashboard no Metabase

#### [Baixar dashboard versão PDF](img/dashboard_metabse_steamAPI.pdf)

O dashboard inclui:

### Overview

-   Total de jogos
-   Total de horas

### Análises por Gênero

-   Quantidade de jogos por Gênero
-   Total de horas

### Engajamento

-   Top 10 Jogos mais jogados
-   Top 10 Jogos menos jogados
-   Jogos mais jogados recentemente

### Interatividade

-   Drill-down por gênero
-   Clique para visualizar jogos individuais

------------------------------------------------------------------------

## Conceitos Aplicados

-   Modelagem analítica
-   Normalização de campo multi-valorado
-   Criação de views para BI
-   Agregações SQL
-   Dockerização de ambiente
-   Persistência de metadata do Metabase em MySQL

------------------------------------------------------------------------

## Objetivo do Projeto

Demonstrar habilidades em:

-   Engenharia de Dados
-   SQL avançado
-   Construção de pipeline
-   Modelagem para BI
-   Criação de dashboards interativos

------------------------------------------------------------------------

## Próximas Evoluções

-   Implementar Star Schema
-   Deploy em ambiente cloud (AWS)
-   Automatização com Airflow
-   Versionamento de views

------------------------------------------------------------------------

## Autor

Cezar Miranda/
Projeto desenvolvido para portfólio de Engenharia de Dados.