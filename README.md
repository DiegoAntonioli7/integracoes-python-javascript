# Serviço de Streaming de Músicas — REST, SOAP e GraphQL

Comparação de **REST**, **SOAP** e **GraphQL** implementados em **Python** e **JavaScript**, com testes de carga via Locust.

## Objetivo

Comparar tecnologias de invocação de serviços remotos em termos de performance, usabilidade e características técnicas.

## Recursos

Gerenciamento de **usuários**, **músicas** e **playlists** (relação N:N entre playlists e músicas). Dados de teste são populados automaticamente via seed ao iniciar cada serviço.

## Estrutura

```
integracoes-python-javascript/
├── rest/          # FastAPI (Python) e Express (JavaScript)
├── soap/          # Spyne (Python) e node-soap (JavaScript)
├── graphql/       # Strawberry (Python) e Apollo (JavaScript)
├── locust/        # Scripts de teste de carga
├── scripts/       # Scripts para subir servidor + Locust
├── results/       # Resultados dos testes
└── docs/          # Documentação detalhada
```

## Pré-requisitos

- Python 3.9+
- Node.js 14+
- Locust: `pip3 install locust`
- Docker (opcional)

## Portas dos serviços

| Serviço | Linguagem | Porta | URL |
|---------|-----------|-------|-----|
| REST | Python | 8000 | http://localhost:8000/api/v1 |
| REST | JavaScript | 3001 | http://localhost:3001/api/v1 |
| SOAP | Python | 8001 | http://localhost:8001/soap |
| SOAP | JavaScript | 3002 | http://localhost:3002/soap |
| GraphQL | Python | 8002 | http://localhost:8002/graphql |
| GraphQL | JavaScript | 3003 | http://localhost:3003/graphql |

## Executar testes (recomendado)

Os scripts em `scripts/` instalam dependências, sobem o servidor correspondente e executam o Locust. Execute a partir da **raiz do repositório**:

```bash
# REST
bash scripts/run_rest_python.sh
bash scripts/run_rest_javascript.sh

# SOAP
bash scripts/run_soap_python.sh
bash scripts/run_soap_javascript.sh

# GraphQL
bash scripts/run_graphql_python.sh
bash scripts/run_graphql_javascript.sh
```

Cada script:

1. Verifica se o Locust está instalado
2. Libera a porta do serviço, se estiver em uso
3. Instala dependências do servidor
4. Sobe o servidor em background
5. Executa o Locust (100 usuários, spawn rate 20)
6. Salva resultados CSV em `{rest|soap|graphql}/results/`

Abra http://localhost:8089 para a interface web do Locust durante a execução.

## Subir um serviço manualmente

```bash
# REST Python
cd rest/python-fastapi-rest && pip3 install -r requirements.txt && uvicorn app:app --port 8000

# REST JavaScript
cd rest/javascript-express-rest && npm install && npm start

# SOAP Python
cd soap/python-spyne-soap && pip3 install -r requirements.txt && python3 app.py

# SOAP JavaScript
cd soap/javascript-node-soap && npm install && npm start

# GraphQL Python
cd graphql/python-strawberry-graphql && pip3 install -r requirements.txt && uvicorn app:app --port 8002

# GraphQL JavaScript
cd graphql/javascript-apollo-graphql && npm install && npm start
```

Para testar manualmente com Locust (em outro terminal, na raiz do projeto):

```bash
locust -f locust/rest_python_locust.py --host http://localhost:8000
```

Substitua o arquivo e a porta conforme o serviço. Veja [docs/como-executar.md](docs/como-executar.md) para o passo a passo completo.

## Docker

```bash
docker-compose up -d    # subir todos os serviços
docker-compose down     # parar
```

## Exemplos rápidos

**GraphQL** — query no playground (`/graphql`):

```graphql
query { users { id name email } }
```

**REST** — listar usuários:

```bash
curl http://localhost:8000/api/v1/users
```

**Seed** (popular banco):

```bash
curl -X POST http://localhost:8000/api/v1/seed          # REST
# GraphQL: mutation { seed }
```

## Comparação resumida

| Critério | REST | SOAP | GraphQL |
|----------|------|------|---------|
| Complexidade | Baixa | Alta | Média |
| Verbosidade | Média | Muito alta | Baixa |
| Ideal para | APIs simples | Integração corporativa | Apps modernas |

## Resultados dos testes de carga

Métricas extraídas dos arquivos `*_stats.csv` gerados pelo Locust (100 usuários, spawn rate 20). Valores da linha **Aggregated** de cada teste.

### Comparativo geral

| Tecnologia | Linguagem | Requisições | Tempo médio (ms) | Tempo mediano (ms) | Tamanho médio da resposta | Throughput (req/s) | Falhas |
|------------|-----------|-------------|------------------|--------------------|---------------------------|--------------------|--------|
| REST | Python | 2.184 | 685,5 | 660 | 127,9 KB | 36,4 | 0 |
| REST | JavaScript | 46.471 | 2,6 | 2 | 129,3 KB | 736,9 | 0 |
| SOAP | Python | 27.504 | 83,9 | 15 | 183,6 KB | 458,3 | 53 |
| SOAP | JavaScript | 36.378 | 2,6 | 2 | 154,2 KB | 724,7 | 0 |
| GraphQL | Python | 6.077 | 72,2 | 68 | 136,4 KB | 101,3 | 0 |

### Comparativo por tecnologia (Python)

| Métrica | REST | SOAP | GraphQL |
|---------|------|------|---------|
| Requisições | 2.184 | 27.504 | 6.077 |
| Tempo médio | 685,5 ms | 83,9 ms | 72,2 ms |
| Tempo mediano | 660 ms | 15 ms | 68 ms |
| Tamanho médio da resposta | 127,9 KB | 183,6 KB | 136,4 KB |
| Throughput | 36,4 req/s | 458,3 req/s | 101,3 req/s |

### Comparativo por tecnologia (JavaScript)

| Métrica | REST | SOAP | GraphQL |
|---------|------|------|---------|
| Requisições | 46.471 | 36.378 | — |
| Tempo médio | 2,6 ms | 2,6 ms | — |
| Tempo mediano | 2 ms | 2 ms | — |
| Tamanho médio da resposta | 129,3 KB | 154,2 KB | — |
| Throughput | 736,9 req/s | 724,7 req/s | — |

> GraphQL JavaScript ainda não possui `stats.csv` em `graphql/results/`. Execute `bash scripts/run_graphql_javascript.sh` para gerar os resultados.

### Principais observações

- **Tamanho da mensagem:** SOAP Python produziu o maior payload (~184 KB), seguido de GraphQL (~136 KB) e REST (~128 KB), refletindo a verbosidade do XML frente ao JSON.
- **Tempo de resposta (Python):** REST Python apresentou o maior tempo médio (~686 ms); GraphQL (~72 ms) e SOAP (~84 ms) foram significativamente mais rápidos no mesmo cenário.
- **Tempo de resposta (JavaScript):** REST e SOAP tiveram desempenho equivalente (~2,6 ms de média), com throughput acima de 720 req/s.
- **Volume de requisições:** REST JavaScript processou o maior número total (46.471); entre as implementações Python, SOAP liderou em volume (27.504 requisições).
- **Confiabilidade:** SOAP Python registrou 53 falhas no teste; as demais implementações concluíram sem erros.

Arquivos de origem: `rest/results/`, `soap/results/` e `graphql/results/`.

## Documentação

- [Como executar](docs/como-executar.md) — guia detalhado de execução
- [Arquitetura](docs/arquitetura.md)
- [Endpoints](docs/endpoints.md)
- [Relatório de testes](docs/relatorio-testes.md)

## Status

| Componente | Status |
|-----------|--------|
| REST / SOAP / GraphQL (Python e JS) | Completo |
| Testes Locust | Completo |
| Docker | Funcional |

---

## Equipe

- **Diego Antonioli** — 
- **Victor Soares** - 1410777

---

