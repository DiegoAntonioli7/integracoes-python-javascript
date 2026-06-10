# Como Executar os Testes

Cada teste Locust requer que o serviço correspondente esteja rodando. Use os scripts em `scripts/` para subir o servidor e iniciar o Locust automaticamente, ou siga o passo a passo manual abaixo.

## Pré-requisito

```bash
pip3 install locust
# Se locust não estiver no PATH, use: python3 -m locust
```

---

## Execução via script (recomendado)

Execute a partir da raiz do repositório:

```bash
# REST Python
bash scripts/run_rest_python.sh

# REST JavaScript
bash scripts/run_rest_javascript.sh

# SOAP Python
bash scripts/run_soap_python.sh

# SOAP JavaScript
bash scripts/run_soap_javascript.sh

# GraphQL Python
bash scripts/run_graphql_python.sh

# GraphQL JavaScript
bash scripts/run_graphql_javascript.sh
```

Cada script instala as dependências, sobe o servidor em background e abre o Locust na interface web (http://localhost:8089).

---

## Execução manual

Cada teste Locust requer que o serviço correspondente esteja rodando. O passo a passo abaixo é independente para cada serviço.

### REST Python (porta 8000)

```bash
cd rest/python-fastapi-rest
pip3 install -r requirements.txt
uvicorn app:app --port 8000
```

Em outro terminal:
```bash
locust -f locust/rest_python_locust.py --host http://localhost:8000
```

---

### REST JavaScript (porta 3001)

```bash
cd rest/javascript-express-rest
npm install
npm start
```

Em outro terminal:
```bash
locust -f locust/rest_javascript_locust.py --host http://localhost:3001
```

---

### SOAP Python (porta 8001)

```bash
cd soap/python-spyne-soap
pip3 install -r requirements.txt
python3 app.py
```

Em outro terminal:
```bash
locust -f locust/soap_python_locust.py --host http://localhost:8001
```

---

### SOAP JavaScript (porta 3002)

```bash
cd soap/javascript-node-soap
npm install
npm start
```

Em outro terminal:
```bash
locust -f locust/soap_javascript_locust.py --host http://localhost:3002
```

---

### GraphQL Python (porta 8002)

```bash
cd graphql/python-strawberry-graphql
pip3 install -r requirements.txt
uvicorn app:app --port 8002
```

Em outro terminal:
```bash
locust -f locust/graphql_python_locust.py --host http://localhost:8002
```

---

### GraphQL JavaScript (porta 3003)

```bash
cd graphql/javascript-apollo-graphql
npm install
npm start
```

Em outro terminal:
```bash
locust -f locust/graphql_javascript_locust.py --host http://localhost:3003
```

---

## Observações

- O seed do banco é feito automaticamente ao iniciar cada teste
- Os comandos `cd` acima são relativos à raiz do repositório
- Apenas um serviço por vez precisa estar rodando para cada teste
- Abrir http://localhost:8089 para acessar a interface do Locust
