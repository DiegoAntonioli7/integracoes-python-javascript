# Serviço de Streaming de Músicas — REST, SOAP e GraphQL

Comparação de **REST**, **SOAP** e **GraphQL** implementados em **Python** e **JavaScript**, com testes de carga via Locust.

## Atualizações desde a última apresentação

Desde a apresentação anterior, foram concluídos os seguintes pontos:

1. **Correção das integrações com JavaScript** — REST (Express), SOAP (node-soap) e GraphQL (Apollo) foram ajustados e validados. As evidências de funcionamento estão na seção [Integrações JavaScript](#integrações-javascript), com capturas de tela do Postman (`docs/imgs/`).
2. **Criação dos gráficos comparativos** — gráficos de tempo de resposta, tamanho do payload e throughput foram gerados a partir dos resultados do Locust. Veja a seção [Gráficos comparativos](#gráficos-comparativos) (`docs/charts/`).
3. **Padronização das integrações para testes justos** — Python passou a usar `sqlite3` puro (conexão persistente, queries diretas), alinhado ao `better-sqlite3` do JavaScript; SOAP Python usa `ThreadingHTTPServer`; payload SOAP unificado (`tns:`/`tns:item`) em ambas as linguagens; Locust roda em modo headless com duração fixa de 60 s em todos os scripts.

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
└── docs/          # Documentação detalhada e capturas de tela (docs/imgs/)
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

## Integrações JavaScript

Além das implementações em Python, o projeto inclui as três tecnologias de integração também em **JavaScript**:

| Tecnologia | Framework | Diretório | Porta |
|------------|-----------|-----------|-------|
| REST | Express | `rest/javascript-express-rest/` | 3001 |
| SOAP | node-soap | `soap/javascript-node-soap/` | 3002 |
| GraphQL | Apollo Server | `graphql/javascript-apollo-graphql/` | 3003 |

Cada serviço expõe os mesmos recursos (usuários, músicas e playlists) e pode ser testado via Postman. As capturas abaixo comprovam o funcionamento das três integrações:

### REST (Express)

Requisição `GET /users` em http://localhost:3001 — resposta JSON com status 200.

<p align="center">
  <img src="docs/imgs/prova-rest-js.png" alt="Postman — GET users no serviço REST JavaScript (Express, porta 3001)" width="900"/>
</p>

### SOAP (node-soap)

Requisição `GetUsers` via POST em http://localhost:3002 — resposta XML com envelope SOAP e status 200.

<p align="center">
  <img src="docs/imgs/prova-soap-js.png" alt="Postman — GetUsers no serviço SOAP JavaScript (node-soap, porta 3002)" width="900"/>
</p>

### GraphQL (Apollo)

Query `{ users { id name email ... } }` em http://localhost:3003/graphql — resposta JSON com status 200.

<p align="center">
  <img src="docs/imgs/prova-graphql-js.png" alt="Postman — query users no serviço GraphQL JavaScript (Apollo, porta 3003)" width="900"/>
</p>

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
5. Executa o Locust em modo headless (100 usuários, spawn rate 20, duração fixa de 60 s)
6. Salva resultados CSV em `{rest|soap|graphql}/results/`

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

Métricas extraídas dos arquivos `*_stats.csv` gerados pelo Locust (100 usuários, spawn rate 20, **60 s** em modo headless). Valores da linha **Aggregated** de cada teste.

> **Nota:** GraphQL Python ainda não foi re-executado após a padronização completa; demais implementações refletem o harness padronizado.

### Comparativo geral

| Tecnologia | Linguagem | Requisições | Tempo médio (ms) | Tempo mediano (ms) | Tamanho médio da resposta | Throughput (req/s) | Falhas |
|------------|-----------|-------------|------------------|--------------------|---------------------------|--------------------|--------|
| REST | Python | 2.360 | 373,0 | 310 | 132,2 KB | 40,0 | 0 |
| REST | JavaScript | 8.919 | 2,9 | 2 | 132,0 KB | 151,0 | 0 |
| SOAP | Python | 3.425 | 218,3 | 200 | 188,2 KB | 57,9 | 1 |
| SOAP | JavaScript | 8.962 | 3,3 | 3 | 188,7 KB | 151,7 | 0 |
| GraphQL | Python | 5.971 | 75,0 | 70 | 140,2 KB | 99,5 | 0 |
| GraphQL | JavaScript | 8.571 | 8,5 | 6 | 132,3 KB | 145,1 | 0 |

### Gráficos comparativos

Valores da linha **Aggregated** de cada teste. Azul = Python, laranja = JavaScript.

#### Tempo de resposta

Comparativo do tempo médio de resposta (ms) entre REST, SOAP e GraphQL.

<p align="center">
  <img src="docs/charts/response_time.png" alt="Gráfico de tempo médio de resposta (ms) — REST, SOAP e GraphQL em Python e JavaScript" width="900"/>
</p>

#### Tamanho do payload

Comparativo do tamanho médio da resposta (KB) — média ponderada dos endpoints `musics`, `playlists` e `users`.

<p align="center">
  <img src="docs/charts/payload_size.png" alt="Gráfico de tamanho médio do payload (KB) — REST, SOAP e GraphQL em Python e JavaScript" width="900"/>
</p>

#### Throughput (req/s)

Comparativo de requisições processadas por segundo.

<p align="center">
  <img src="docs/charts/throughput.png" alt="Gráfico de throughput (req/s) — REST, SOAP e GraphQL em Python e JavaScript" width="900"/>
</p>

Arquivos fonte (SVG): `docs/charts/response_time.svg`, `docs/charts/payload_size.svg`, `docs/charts/throughput.svg`.

Para regenerar os gráficos após novos testes:

```bash
python3 scripts/generate_benchmark_charts.py
```

### Comparativo por tecnologia (Python)

| Métrica | REST | SOAP | GraphQL |
|---------|------|------|---------|
| Requisições | 2.360 | 3.425 | 5.971 |
| Tempo médio | 373,0 ms | 218,3 ms | 75,0 ms |
| Tempo mediano | 310 ms | 200 ms | 70 ms |
| Tamanho médio da resposta | 132,2 KB | 188,2 KB | 140,2 KB |
| Throughput | 40,0 req/s | 57,9 req/s | 99,5 req/s |
| Falhas | 0 | 1 | 0 |

### Comparativo por tecnologia (JavaScript)

| Métrica | REST | SOAP | GraphQL |
|---------|------|------|---------|
| Requisições | 8.919 | 8.962 | 8.571 |
| Tempo médio | 2,9 ms | 3,3 ms | 8,5 ms |
| Tempo mediano | 2 ms | 3 ms | 6 ms |
| Tamanho médio da resposta | 132,0 KB | 188,7 KB | 132,3 KB |
| Throughput | 151,0 req/s | 151,7 req/s | 145,1 req/s |
| Falhas | 0 | 0 | 0 |

### Tamanho do payload por endpoint

As tabelas acima usam a linha **Aggregated** do Locust: média ponderada dos três endpoints, com pesos 3:2:1 (`musics` / `playlists` / `users`) no script Locust. Para comparar verbosidade de protocolo, o mesmo recurso deve ser analisado isoladamente — em geral `musics`, o maior payload.

| Endpoint | REST Python | REST JS | SOAP Python | SOAP JS | GraphQL Python | GraphQL JS |
|----------|-------------|---------|-------------|---------|----------------|------------|
| musics | 168,5 KB | 168,5 KB | **247,7 KB** | **247,7 KB** | 178,5 KB | 168,5 KB |
| playlists | 113,0 KB | 113,0 KB | **151,2 KB** | **151,4 KB** | 117,8 KB | 113,0 KB |
| users | 60,7 KB | 60,7 KB | **84,0 KB** | **84,0 KB** | 63,9 KB | 60,7 KB |
| **Aggregated** | 132,2 KB | 132,0 KB | **188,2 KB** | **188,7 KB** | 140,2 KB | 132,3 KB |

SOAP é o protocolo com maior payload em todos os endpoints e linguagens — coerente com a verbosidade do XML. REST e GraphQL JavaScript ficam praticamente iguais (~132 KB); GraphQL Python fica um pouco acima por causa do envelope JSON (`{"data":{"musics":[...]}}`). Após a padronização, SOAP Python e JavaScript usam o mesmo formato XML (`tns:`/`tns:item`) e produzem payloads equivalentes (~188 KB agregado).

### Principais observações

- **Tamanho da mensagem (coerente):** SOAP é o maior em cada endpoint e linguagem (~188 KB agregado); REST e GraphQL JavaScript ficam equivalentes (~132 KB); GraphQL Python fica entre REST e SOAP (~140 KB) pelo envelope JSON.
- **Tempo de resposta (Python):** GraphQL (~75 ms) foi o mais rápido; SOAP (~218 ms) ficou no meio; REST (~373 ms) foi o mais lento. A ordem REST < GraphQL < SOAP em velocidade **ainda não se confirma** em Python.
- **Tempo de resposta (JavaScript, coerente):** REST (~2,9 ms) foi o mais rápido; SOAP (~3,3 ms) ficou no meio apesar do payload ~43% maior; GraphQL (~8,5 ms) foi o mais lento — overhead do Apollo Server supera a verbosidade do SOAP.
- **Volume de requisições:** Com 60 s fixos, JavaScript processou ~8.570–8.960 requisições em todos os protocolos; Python variou de 2.360 (REST) a 5.971 (GraphQL), refletindo diferenças de throughput.
- **Confiabilidade:** SOAP Python registrou 1 falha (`GetPlaylists`) por concorrência no SQLite; todas as implementações JavaScript e demais testes Python concluíram sem falhas (exceto essa).

### O que mudou com a padronização

Foram corrigidas as principais fontes de distorção identificadas na análise anterior:

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Acesso ao banco (Python) | SQLAlchemy ORM + sessão por requisição | `sqlite3` puro, conexão persistente, `SELECT *` direto |
| Concorrência SOAP Python | `HTTPServer` single-thread | `ThreadingHTTPServer` |
| Payload SOAP | Formatos diferentes (Python `tns:` vs JS sem prefixo) | Formato unificado `tns:`/`tns:item` |
| Duração do teste | Variável (parada manual) | Fixa: 60 s headless em todos os scripts |

Com isso, a lacuna artificial entre SOAP Python (~5 ms) e REST Python (~326 ms) desapareceu — ambos passaram a operar na mesma faixa de dezenas a centenas de ms.

### Análise dos resultados atuais

#### 1. Payload — coerente com a teoria

SOAP produz respostas ~43% maiores que REST/GraphQL JS no agregado (~188 KB vs ~132 KB). GraphQL Python fica entre os dois (~140 KB) por causa do envelope JSON. **O tamanho da mensagem segue a ordem esperada: REST ≈ GraphQL < SOAP.**

#### 2. Tempo de resposta — Python vs JavaScript

**Python** — REST permanece o gargalo:

| Python | Tempo médio | Throughput | Tempo médio `/musics` |
|--------|-------------|------------|------------------------|
| GraphQL | 75,0 ms | 99,5 req/s | ~75 ms |
| SOAP | 218,3 ms | 57,9 req/s | ~303 ms |
| REST | 373,0 ms | 40,0 req/s | ~510 ms |

**JavaScript** — ordem coerente com a teoria (REST mais rápido):

| JavaScript | Tempo médio | Throughput | Tempo médio `/musics` |
|------------|-------------|------------|------------------------|
| REST | 2,9 ms | 151,0 req/s | ~3,4 ms |
| SOAP | 3,3 ms | 151,7 req/s | ~3,9 ms |
| GraphQL | 8,5 ms | 145,1 req/s | ~9,8 ms |

Em JavaScript, REST é o mais rápido e GraphQL o mais lento — o custo do Apollo (parse de query, resolução de campos) supera a verbosidade do XML do SOAP. Em Python, FastAPI/uvicorn ainda satura mais que SOAP e GraphQL.

#### 3. Python vs JavaScript — gap de runtime

Mesmo com banco padronizado (`sqlite3` / `better-sqlite3`), **Node.js + V8** mantém tempos de ~3–9 ms vs ~75–373 ms do **Python + uvicorn** — diferença de uma a duas ordens de magnitude na mesma operação.

#### 4. Falha no SOAP Python

Durante o teste, 1 requisição `GetPlaylists` falhou com `RemoteDisconnected` — causada por `IndexError` ao acessar `sqlite3.Row` concorrentemente no `ThreadingHTTPServer`. Indica necessidade de lock na conexão SQLite ou conexão por thread.

#### Resumo: o que os números comparam agora

| O que parece ser comparado | O que está sendo medido de fato |
|----------------------------|--------------------------------|
| REST vs SOAP vs GraphQL | Framework + serialização + runtime sob carga |
| Python vs JavaScript | uvicorn/FastAPI vs Node.js/V8 (banco agora alinhado) |
| Tamanho do payload | Verbosidade real do protocolo (coerente) |
| Tempo de resposta | Tempo total incluindo fila, com 100 usuários por 60 s |

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

