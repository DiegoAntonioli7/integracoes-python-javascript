# 🎵 Serviço de Streaming de Músicas - Comparação REST, SOAP e GraphQL

## 📖 Visão Geral

Este projeto implementa um **serviço de streaming de músicas** em 3 tecnologias diferentes de invocação de serviços remotos:

- ✅ **REST** - Arquitetura representacional de estado
- ✅ **SOAP** - Protocolo simples de acesso a objetos (XML)
- ✅ **GraphQL** - Linguagem de query para APIs

Cada tecnologia foi implementada em **Python** e **JavaScript** para análise comparativa de performance, usabilidade e características.

---

## 🎯 Objetivo do Projeto

Comparar e analisar as principais características de 3 tecnologias de invocação de serviços remotos através de:

1. **Implementação funcional** em Python e JavaScript
2. **Análise técnica** de origem, características, vantagens e desvantagens
3. **Testes de carga** comparativos usando Locust
4. **Relatório crítico** com gráficos de performance

---

## 📊 Recursos Gerenciados

O serviço permite gerenciamento de 3 tipos de recursos:

### 👥 Usuários
- Identificação única (UUID)
- Nome, email, país e cidade
- Bio, telefone e avatar
- Relacionamento com múltiplas playlists

### 🎵 Músicas
- Título, artista, álbum
- Duração em segundos
- Gênero, gravadora, compositor
- Snippet de letras e URL da capa

### 📋 Playlists
- Pertence a um usuário específico
- Contém múltiplas músicas (relação N:N)
- Nome, descrição, tags de gênero, mood
- Notas customizáveis

---

## 🏗️ Estrutura do Projeto

```
integracoes-python-javascript/
├── rest/
│   ├── python-fastapi-rest/          # FastAPI REST
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── README.md
│   └── javascript-express-rest/      # Express REST
│       ├── app.js
│       ├── package.json
│       └── README.md
│
├── soap/
│   ├── python-spyne-soap/            # Spyne SOAP
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── README.md
│   └── javascript-node-soap/         # Node-SOAP
│       ├── app.js
│       ├── package.json
│       └── README.md
│
├── graphql/
│   ├── python-strawberry-graphql/    # Strawberry GraphQL
│   │   ├── app.py
│   │   ├── schema.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── requirements.txt
│   │   └── README.md
│   └── javascript-apollo-graphql/    # Apollo GraphQL
│       ├── app.js
│       ├── package.json
│       └── README.md
│
├── locust/                           # Testes de Carga
│   ├── rest_python_locust.py
│   ├── rest_javascript_locust.py
│   ├── soap_python_locust.py
│   ├── soap_javascript_locust.py
│   ├── graphql_python_locust.py
│   └── graphql_javascript_locust.py
│
├── results/                          # Resultados dos Testes
│   ├── rest/
│   ├── soap/
│   └── graphql/
│
├── docs/
│   ├── arquitetura.md               # Documentação de arquitetura
│   ├── endpoints.md                 # Documentação de endpoints
│   ├── relatorio-testes.md          # Template de relatório
│   └── PLANO_ACAO.md                # Plano de implementação
│
├── docker-compose.yml               # Orquestração de containers
├── README.md                        # Este arquivo
└── shared/
    └── seed_data.py                 # Dados de teste compartilhados
```

---

## 🚀 Como Começar

### Pré-requisitos

- **Python 3.9+** (para serviços Python)
- **Node.js 14+** (para serviços JavaScript)
- **Docker** e **Docker Compose** (opcional, para containerização)
- **Locust** (para testes de carga)

### Instalação Rápida

#### 1️⃣ GraphQL Python (Strawberry)

```bash
cd graphql/python-strawberry-graphql
pip install -r requirements.txt
python app.py
```

**Acesso:**
- GraphQL Endpoint: `http://localhost:8002/graphql`
- GraphQL Playground: `http://localhost:8002/graphql` (IDE interativa)
- Health Check: `http://localhost:8002/health`

#### 2️⃣ GraphQL JavaScript (Apollo)

```bash
cd graphql/javascript-apollo-graphql
npm install
node app.js
```

**Acesso:**
- GraphQL Endpoint: `http://localhost:3003/graphql`
- GraphQL Playground: `http://localhost:3003/graphql`
- Health Check: `http://localhost:3003/health`

#### 3️⃣ Executar Todos os Serviços (Docker)

```bash
docker-compose up
```

---

## 📡 Tecnologias Implementadas

### 🔴 REST (Representational State Transfer)

**Características:**
- Arquitetura simples e baseada em recursos
- Usa métodos HTTP padrão (GET, POST, PUT, DELETE)
- Stateless
- Fácil cache
- Payload em JSON

**Implementações:**
- **Python**: FastAPI + Pydantic + SQLAlchemy
- **JavaScript**: Express.js + Sequelize

**Base URLs:**
- Python: `http://localhost:8000/api/v1`
- JavaScript: `http://localhost:3001/api/v1`

**Endpoints principais:**
- `GET /users` - Listar usuários
- `POST /users` - Criar usuário
- `GET /musics` - Listar músicas
- `GET /playlists` - Listar playlists
- `GET /users/{id}/playlists` - Playlists de um usuário

### 🟠 SOAP (Simple Object Access Protocol)

**Características:**
- Baseado em XML
- Mais verboso que REST
- Suporta transações complexas
- WS-Security para segurança
- Melhor para APIs corporativas complexas

**Implementações:**
- **Python**: Spyne (geração automática de WSDL)
- **JavaScript**: node-soap + better-sqlite3

**Base URLs:**
- Python: `http://localhost:8001/soap`
- JavaScript: `http://localhost:3002/soap`

**Web Services:**
- UserService
- MusicService
- PlaylistService

### 🟢 GraphQL (Graph Query Language)

**Características:**
- Linguagem de query declarativa
- Uma única requisição para dados complexos
- Tipagem forte (Schema)
- Resolvers para dados relacionados
- Introspection e playground integrado

**Implementações:**
- **Python**: Strawberry (type-based, moderno)
- **JavaScript**: Apollo Server 4

**Base URLs:**
- Python: `http://localhost:8002/graphql`
- JavaScript: `http://localhost:3003/graphql`

**Principais tipos:**
- `User` - Usuários com playlists
- `Music` - Músicas com playlists relacionadas
- `Playlist` - Playlists com usuário e músicas

---

## 📚 Exemplos de Uso

### GraphQL - Python Strawberry

#### Query - Listar Usuários
```graphql
query {
  users {
    id
    name
    email
    country
    city
    bio
  }
}
```

#### Query - Playlists de um Usuário
```graphql
query {
  userPlaylists(userId: "user-id-123") {
    id
    name
    description
    musics {
      id
      title
      artist
      album
      duration
    }
  }
}
```

#### Query - Playlists que Contêm uma Música
```graphql
query {
  musicPlaylists(musicId: "music-id-456") {
    id
    name
    user {
      name
      email
    }
  }
}
```

#### Mutation - Seed (Inicializar Dados)
```graphql
mutation {
  seed
}
```

### GraphQL - JavaScript Apollo

Mesmas queries acima funcionam em `http://localhost:3003/graphql`

### REST - Python FastAPI

#### Listar Usuários (cURL)
```bash
curl -X GET http://localhost:8000/api/v1/users
```

#### Criar Usuário
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "country": "Brasil",
    "city": "São Paulo",
    "bio": "Amante de música",
    "phone": "+55 11 98765-4321",
    "avatar_url": "https://example.com/avatar.jpg"
  }'
```

#### Listar Playlists de um Usuário
```bash
curl -X GET http://localhost:8000/api/v1/users/user-id/playlists
```

### REST - JavaScript Express

Mesmos endpoints em `http://localhost:3001/api/v1`

### SOAP - Python Spyne

#### GetUsers (XML Request)
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns0:GetUsers xmlns:ns0="http://streaming.api/users"/>
  </soap:Body>
</soap:Envelope>
```

#### CreateUser
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns0:CreateUser xmlns:ns0="http://streaming.api/users">
      <ns0:name>João Silva</ns0:name>
      <ns0:email>joao@example.com</ns0:email>
      <ns0:country>Brasil</ns0:country>
      <ns0:city>São Paulo</ns0:city>
    </ns0:CreateUser>
  </soap:Body>
</soap:Envelope>
```

### SOAP - JavaScript node-soap

Mesmos serviços em `http://localhost:3002/soap`

---

## 🧪 Testes de Carga

### Usando Locust

Os testes de carga são definidos em scripts Python usando **Locust**, uma ferramenta de teste de carga fácil de usar.

#### Instalar Locust
```bash
pip install locust
```

#### Executar Teste de Carga - GraphQL Python
```bash
locust -f locust/graphql_python_locust.py --host=http://localhost:8002
```

#### Executar Teste de Carga - GraphQL JavaScript
```bash
locust -f locust/graphql_javascript_locust.py --host=http://localhost:3003
```

#### Executar Teste de Carga - REST Python
```bash
locust -f locust/rest_python_locust.py --host=http://localhost:8000
```

#### Executar Teste de Carga - REST JavaScript
```bash
locust -f locust/rest_javascript_locust.py --host=http://localhost:3001
```

**Interface Web Locust:**
- Acesse: `http://localhost:8089`
- Configure número de usuários e requisições/seg
- Monitore em tempo real

### Cenários de Teste Recomendados

1. **Teste Leve**: 10 usuários, 100 req/seg, 2 minutos
2. **Teste Médio**: 50 usuários, 500 req/seg, 5 minutos
3. **Teste Pesado**: 100 usuários, 1000 req/seg, 10 minutos

### Métricas Coletadas

- ✅ Response Time (média, mediana, P95, P99, min, max)
- ✅ Throughput (requisições por segundo)
- ✅ Taxa de erro (%)
- ✅ Consumo de CPU (%)
- ✅ Consumo de memória (MB)
- ✅ Tamanho de payload (request/response em KB)
- ✅ Número de conexões simultâneas

---

## 📊 Dados de Teste

O projeto inclui dados de teste automáticos via seeding:

**Quantidade de dados:**
- **5 usuários** com perfis completos
- **20 músicas** variadas com metadados completos
- **10 playlists** pré-configuradas
- Relacionamentos N:N entre playlists e músicas

**Acessar dados de teste:**

**GraphQL:**
```graphql
mutation {
  seed
}
```

**REST:**
```bash
curl -X POST http://localhost:8000/api/v1/seed
```

**SOAP:**
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns0:Seed xmlns:ns0="http://streaming.api"/>
  </soap:Body>
</soap:Envelope>
```

---

## 🛠️ Arquitetura

### Camadas de Aplicação

```
┌─────────────────────────────────────────────┐
│   API Layer (HTTP/SOAP/GraphQL)            │
│   REST | SOAP | GraphQL                     │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│   Service Layer                             │
│   UserService, MusicService, PlaylistService│
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│   Data Access Layer (ORM)                   │
│   SQLAlchemy (Python) / better-sqlite3 (JS)│
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│   Database Layer                            │
│   SQLite (dev) / PostgreSQL (production)    │
└─────────────────────────────────────────────┘
```

### Banco de Dados

**Tabelas:**
- `users` - Usuários do serviço
- `musics` - Acervo de músicas
- `playlists` - Coleções de usuários
- `playlist_music` - Relacionamento N:N (Junction Table)

**Schema Completo:**

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  country TEXT,
  city TEXT,
  bio TEXT,
  phone TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE musics (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  album TEXT,
  duration INTEGER,
  genre TEXT,
  label TEXT,
  composer TEXT,
  lyrics_snippet TEXT,
  cover_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE playlists (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  genre_tags TEXT,
  mood TEXT,
  cover_url TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE playlist_music (
  playlist_id TEXT NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
  music_id TEXT NOT NULL REFERENCES musics(id) ON DELETE CASCADE,
  PRIMARY KEY (playlist_id, music_id)
);

CREATE INDEX idx_user_id ON playlists(user_id);
CREATE INDEX idx_music_playlist ON playlist_music(music_id);
```

### Relacionamentos

```
User (1) ──── (N) Playlist
              ↓
          (N) ── (N) Music
              playlist_music
```

---

## 📈 Comparação de Tecnologias

| Critério | REST | SOAP | GraphQL |
|----------|------|------|---------|
| **Complexidade** | Baixa | Alta | Média |
| **Verbosidade** | Média | Muito Alta | Baixa |
| **Performance** | Boa | Aceitável | Excelente |
| **Curva de Aprendizado** | Fácil | Difícil | Média |
| **Tipagem** | Opcional | Implícita | Forte |
| **Caching** | Fácil (HTTP) | Difícil | Médio |
| **Overhead** | Baixo | Alto (XML) | Médio (JSON) |
| **Suporte a Versioning** | Múltiplos URLs | Namespace | Schema Evolution |
| **Payload Size** | Médio | Grande | Otimizado |
| **Ideal Para** | APIs simples | Integração corporativa | Apps modernas |

---

## 🔧 Desenvolvimento

### Setup para Contribuição

```bash
# Clone o repositório
git clone https://github.com/DiegoAntonioli7/integracoes-python-javascript.git
cd integracoes-python-javascript

# Crie um virtualenv (Python)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### Estrutura de Branches

```
main (produção)
├── feature/* (novas funcionalidades)
├── fix/* (correções de bugs)
├── test/* (melhorias em testes)
└── docs/* (atualizações de documentação)
```

### Adicionando Nova Funcionalidade

1. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
2. Implemente em Python E JavaScript (em paralelo)
3. Adicione testes em Locust
4. Documente em `/docs`
5. Faça push e abra um Pull Request

---

## 🐳 Docker Support

### Executar com Docker Compose

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar serviços
docker-compose down

# Remover volumes (dados persistidos)
docker-compose down -v
```

### Verificar Status

```bash
# Listar containers rodando
docker-compose ps

# Acessar logs específicos
docker-compose logs rest-python
docker-compose logs graphql-javascript
```

### Ports Mapeadas

| Serviço | Tipo | Versão | Port | URL |
|---------|------|--------|------|-----|
| REST | Python | FastAPI | 8000 | http://localhost:8000 |
| REST | JavaScript | Express | 3001 | http://localhost:3001 |
| SOAP | Python | Spyne | 8001 | http://localhost:8001/soap |
| SOAP | JavaScript | node-soap | 3002 | http://localhost:3002/soap |
| GraphQL | Python | Strawberry | 8002 | http://localhost:8002/graphql |
| GraphQL | JavaScript | Apollo | 3003 | http://localhost:3003/graphql |
| Locust | Monitor | Web UI | 8089 | http://localhost:8089 |
| PostgreSQL | DB | 13 | 5432 | localhost:5432 |

---

## 📝 Scripts Úteis

### Health Checks

```bash
# Python GraphQL
curl http://localhost:8002/health

# JavaScript GraphQL
curl http://localhost:3003/health

# REST Python
curl http://localhost:8000/health

# REST JavaScript
curl http://localhost:3001/health
```

### Teste de Query GraphQL

```bash
# Python
curl -X POST http://localhost:8002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name email } }"}'

# JavaScript
curl -X POST http://localhost:3003/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name email } }"}'
```

### Teste de REST

```bash
# Listar usuários
curl http://localhost:8000/api/v1/users

# Listar músicas
curl http://localhost:8000/api/v1/musics

# Listar playlists
curl http://localhost:8000/api/v1/playlists
```

### Executar Testes de Carga em Linha de Comando

```bash
# GraphQL Python (headless)
locust -f locust/graphql_python_locust.py \
  --host=http://localhost:8002 \
  --users=50 \
  --spawn-rate=10 \
  --run-time=5m \
  --headless

# Exportar resultados
locust -f locust/graphql_python_locust.py \
  --host=http://localhost:8002 \
  --html=results/graphql_python_report.html
```

---

## 📚 Documentação Detalhada

- 📖 **[Arquitetura](docs/arquitetura.md)** - Design de sistema, padrões, diagramas
- 📋 **[Endpoints](docs/endpoints.md)** - Documentação completa de todas as APIs
- 📊 **[Plano de Ação](docs/PLANO_ACAO.md)** - Roadmap detalhado de implementação
- 📈 **[Relatório de Testes](docs/relatorio-testes.md)** - Template e guia de análise

---

## 🔍 Troubleshooting

### Erro: "Port already in use"

```bash
# Verificar processo usando a porta
lsof -i :8002  # Linux/Mac
netstat -an | findstr :8002  # Windows

# Liberar porta ou usar outra
# Edite docker-compose.yml ou .env
```

### Erro: "Database locked" (SQLite)

```bash
# SQLite tem limite de conexões simultâneas
# Para produção, use PostgreSQL
# Veja docker-compose.yml para configuração
```

### Erro: "npm install não funciona"

```bash
# Limpar cache npm
npm cache clean --force

# Instalar novamente
npm install
```

### GraphQL Playground não abre

- Verifique se introspection está habilitado
- Acesse diretamente: `http://localhost:PORT/graphql`
- Teste query simples: `{ __schema { types { name } } }`

---

## 📚 Referências Acadêmicas

1. **REST**: [Fielding Dissertation - Architectural Styles and the Design of Network-Based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
2. **SOAP**: [W3C SOAP 1.2 Part 1: Messaging Framework](https://www.w3.org/TR/soap12/)
3. **GraphQL**: [GraphQL: A query language for your API](https://graphql.org/)
4. **Comparação**: [REST vs GraphQL: A Controlled Experiment (ICSA 2020)](https://www.researchgate.net/publication/339413273_REST_vs_GraphQL_A_Controlled_Experiment)

### Tecnologias

- **FastAPI**: [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **Strawberry**: [Strawberry GraphQL](https://strawberry.rocks/)
- **Apollo**: [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- **Express**: [Express.js](https://expressjs.com/)
- **Spyne**: [Spyne SOAP Framework](https://spyne.io/)
- **Locust**: [Locust Load Testing](https://locust.io/)

---

## 👥 Equipe

- **Diego Antonioli** ([@DiegoAntonioli7](https://github.com/DiegoAntonioli7))

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes

```
MIT License

Copyright (c) 2024 Diego Antonioli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. **Fork** o projeto (`git clone https://github.com/SEU_USUARIO/integracoes-python-javascript.git`)
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Diretrizes

- ✅ Implemente em AMBAS as linguagens (Python e JavaScript)
- ✅ Adicione testes correspondentes em Locust
- ✅ Atualize documentação em `/docs`
- ✅ Mantenha consistência de código (use linters)
- ✅ Adicione exemplos de uso no README

---

## 📧 Suporte e Contato

Para dúvidas, sugestões ou reportar bugs:

1. **Abra uma Issue** no GitHub
2. **Envie um email** (verifique profile)
3. **Discuta** em Discussions (se disponível)

---

## 🎓 Uso Educacional

Este projeto foi desenvolvido para fins **educacionais** e de **pesquisa** em Computação Distribuída, como parte de um projeto acadêmico comparativo entre tecnologias de invocação de serviços remotos.

**Referência de Trabalho Acadêmico:**
> Trabalho 6 – Comparação de Tecnologias de Invocação de Serviços Remotos
> Computação Distribuída - Prof. Nabor C. Mendonça

---

## 🎉 Status do Projeto

| Componente | Status | Implementação |
|-----------|--------|--------------|
| REST Python | ✅ | Completo |
| REST JavaScript | ✅ | Completo |
| SOAP Python | ✅ | Completo |
| SOAP JavaScript | ✅ | Completo |
| GraphQL Python | ✅ | Completo |
| GraphQL JavaScript | ✅ | Completo |
| Testes Locust | 🔄 | Em desenvolvimento |
| Documentação | ✅ | Completa |
| Docker Support | ✅ | Funcional |

---

**Desenvolvido com ❤️ para fins educacionais e comparativos** 🎓

Last updated: Junho 2024
