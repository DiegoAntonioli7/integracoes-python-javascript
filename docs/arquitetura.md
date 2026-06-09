# Arquitetura - Serviço de Streaming de Músicas

## 🎯 Visão Geral

Este documento descreve a arquitetura do serviço de streaming de músicas implementado em 3 tecnologias diferentes (REST, SOAP, GraphQL) em Python e JavaScript para comparação de performance e características.

## 📐 Diagrama de Entidades

```
┌─────────────┐
│   User      │
├─────────────┤
│ id (PK)     │
│ name        │
│ email       │
└─────────────┘
      │
      │ 1:N
      ↓
┌─────────────────┐
│   Playlist      │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ name            │
│ description     │
└─────────────────┘
      │
      │ N:N
      ↓
┌─────────────┐
│   Music     │
├─────────────┤
│ id (PK)     │
│ title       │
│ artist      │
│ album       │
│ duration    │
└─────────────┘
```

## 🏗️ Camadas de Arquitetura

```
┌─────────────────────────────────────┐
│      API Layer (HTTP)               │
│  REST | SOAP | GraphQL              │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│      Service Layer                  │
│  UserService, MusicService, etc.    │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│      Data Access Layer              │
│  SQLAlchemy / Sequelize / TypeORM   │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│      Database Layer                 │
│  SQLite / PostgreSQL                │
└─────────────────────────────────────┘
```

## 🔄 Fluxo de Requisição

### REST
```
Client → HTTP Request → Express/FastAPI → Service Layer → Database → Response (JSON) → Client
```

### SOAP
```
Client → SOAP Request (XML) → Spyne/node-soap → Service Layer → Database → SOAP Response (XML) → Client
```

### GraphQL
```
Client → GraphQL Query/Mutation → Apollo/Strawberry → Resolvers → Service Layer → Database → JSON Response → Client
```

## 📦 Modelos de Dados

### User
```json
{
  "id": "uuid",
  "name": "string",
  "email": "string",
  "created_at": "2024-06-09T10:30:00Z"
}
```

### Music
```json
{
  "id": "uuid",
  "title": "string",
  "artist": "string",
  "album": "string",
  "duration": 180,
  "created_at": "2024-06-09T10:30:00Z"
}
```

### Playlist
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "description": "string",
  "music_ids": ["uuid1", "uuid2"],
  "created_at": "2024-06-09T10:30:00Z"
}
```

## 🔌 Pontos de Integração

### Python-JavaScript Communication
- Ambos expõem as mesmas APIs
- Clientes podem escolher entre implementações
- Mesmas operações disponíveis

### Banco de Dados Compartilhado
- Opção: Usar mesmo banco para ambas as implementações
- Ou: Separar e comparar sincronização

## 🚀 Padrões de Design

### Service Layer Pattern
- Lógica de negócio centralizada
- Fácil manutenção e testes
- Reutilizável entre tecnologias

### Repository Pattern
- Abstração da camada de dados
- Facilita testes com mocks
- Muda fácil entre bancos

### Dependency Injection
- Framework handle automático (FastAPI, Express)
- Reduz acoplamento
- Facilita testes

## 🔐 Considerações de Segurança

- [ ] Validação de entrada em todas camadas
- [ ] Sanitização de dados
- [ ] CORS configuration
- [ ] Rate limiting
- [ ] Autenticação básica (JWT opcional)

## 📈 Performance Considerations

### Caching
- Cache de queries frequentes
- TTL configurável

### Paginação
- Implementar para grandes datasets
- Reduz payload

### Indexação DB
- Índices em user_id, music_id
- Melhora queries relacionadas

### Lazy Loading
- Carregar playlists/músicas sob demanda
- Reduz memory footprint

---

## 📋 Versionamento de API

### REST
```
/api/v1/users
/api/v2/users (future)
```

### SOAP
```
Namespace: http://streaming.api.com/v1
```

### GraphQL
```
Schema versioning via mutations e queries
```

---

## 🧪 Estratégia de Testes

### Testes Unitários
- Mocks de database
- Testes de validação

### Testes de Integração
- Banco de dados em memória
- Fluxos completos

### Testes de Carga
- Locust scripts
- Múltiplos cenários

---

## 📊 Monitoramento

### Métricas a Coletar
- Response time
- Throughput
- Taxa de erro
- Consumo de recursos

### Logging
- Request/Response logs
- Error logs
- Performance logs

