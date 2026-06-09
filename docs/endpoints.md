# API Endpoints Documentation

## 🎵 Serviço de Streaming de Músicas - Endpoints

### Base URLs
- **REST Python**: `http://localhost:8000/api/v1`
- **REST JavaScript**: `http://localhost:3001/api/v1`
- **SOAP Python**: `http://localhost:8001/soap`
- **SOAP JavaScript**: `http://localhost:3002/soap`
- **GraphQL Python**: `http://localhost:8002/graphql`
- **GraphQL JavaScript**: `http://localhost:3003/graphql`

---

## 👥 Users Endpoints

### REST

#### List All Users
```http
GET /users
Content-Type: application/json

Response: 200 OK
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    "email": "joao@example.com",
    "created_at": "2024-06-09T10:30:00Z"
  }
]
```

#### Create User
```http
POST /users
Content-Type: application/json

Body:
{
  "name": "Maria Santos",
  "email": "maria@example.com"
}

Response: 201 Created
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Maria Santos",
  "email": "maria@example.com",
  "created_at": "2024-06-09T10:30:00Z"
}
```

#### Update User
```http
PUT /users/{id}
Content-Type: application/json

Body:
{
  "name": "Maria Silva",
  "email": "maria.silva@example.com"
}
```

#### Delete User
```http
DELETE /users/{id}

Response: 204 No Content
```

---

## 🎵 Music Endpoints

### REST

#### List All Musics
```http
GET /musics
Response: 200 OK
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Shape of You",
    "artist": "Ed Sheeran",
    "album": "÷ (Divide)",
    "duration": 233,
    "created_at": "2024-06-09T10:30:00Z"
  }
]
```

#### Create Music
```http
POST /musics
Content-Type: application/json

Body:
{
  "title": "Shape of You",
  "artist": "Ed Sheeran",
  "album": "÷ (Divide)",
  "duration": 233
}
```

#### Update Music
```http
PUT /musics/{id}
Content-Type: application/json

Body:
{
  "title": "Shape of You - Remix",
  "duration": 240
}
```

#### Delete Music
```http
DELETE /musics/{id}
Response: 204 No Content
```

---

## 📋 Playlist Endpoints

### REST

#### List All Playlists
```http
GET /playlists?page=1&limit=20
Response: 200 OK
{
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Favoritas",
      "description": "Minhas músicas favoritas",
      "created_at": "2024-06-09T10:30:00Z"
    }
  ],
  "total": 100,
  "page": 1
}
```

#### Get User's Playlists
```http
GET /users/{user_id}/playlists
Response: 200 OK
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "name": "Favoritas",
    "description": "Minhas músicas favoritas",
    "musicCount": 15
  }
]
```

#### Get Musics in Playlist
```http
GET /playlists/{playlist_id}/musics
Response: 200 OK
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Shape of You",
    "artist": "Ed Sheeran",
    "duration": 233
  }
]
```

#### Get Playlists Containing a Music
```http
GET /musics/{music_id}/playlists
Response: 200 OK
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "name": "Favoritas",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  }
]
```

#### Create Playlist
```http
POST /playlists
Content-Type: application/json

Body:
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Favoritas",
  "description": "Minhas músicas favoritas"
}

Response: 201 Created
```

#### Add Music to Playlist
```http
POST /playlists/{playlist_id}/musics/{music_id}
Response: 200 OK
```

#### Remove Music from Playlist
```http
DELETE /playlists/{playlist_id}/musics/{music_id}
Response: 204 No Content
```

#### Update Playlist
```http
PUT /playlists/{id}
Content-Type: application/json

Body:
{
  "name": "Favoritas 2024",
  "description": "Novas favoritas"
}
```

#### Delete Playlist
```http
DELETE /playlists/{id}
Response: 204 No Content
```

---

## 🔄 GraphQL Queries & Mutations

### Query All Users
```graphql
query {
  users {
    id
    name
    email
    createdAt
  }
}
```

### Query User's Playlists
```graphql
query {
  userPlaylists(userId: "550e8400-e29b-41d4-a716-446655440000") {
    id
    name
    description
    musics {
      id
      title
      artist
      duration
    }
  }
}
```

### Query Music Playlists
```graphql
query {
  musicPlaylists(musicId: "660e8400-e29b-41d4-a716-446655440000") {
    id
    name
    user {
      name
      email
    }
  }
}
```

### Create User Mutation
```graphql
mutation {
  createUser(input: {
    name: "João Silva"
    email: "joao@example.com"
  }) {
    id
    name
    email
  }
}
```

### Add Music to Playlist Mutation
```graphql
mutation {
  addMusicToPlaylist(
    playlistId: "770e8400-e29b-41d4-a716-446655440000"
    musicId: "660e8400-e29b-41d4-a716-446655440000"
  ) {
    id
    musics {
      id
      title
    }
  }
}
```

---

## 📊 Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## 📖 Exemplos de Cliente

### cURL
```bash
# Get all users
curl -X GET http://localhost:8000/api/v1/users

# Create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "João", "email": "joao@example.com"}'
```

### Python (requests)
```python
import requests

response = requests.get('http://localhost:8000/api/v1/users')
users = response.json()
```

### JavaScript (fetch)
```javascript
const response = await fetch('http://localhost:3001/api/v1/users');
const users = await response.json();
```

