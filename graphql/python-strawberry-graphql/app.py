import sqlite3
import sys
from pathlib import Path
from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DB_PATH = Path(__file__).parent / "graphql_python.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row

SCHEMA = """
DROP TABLE IF EXISTS playlist_music;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS musics;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id TEXT PRIMARY KEY, name TEXT, email TEXT, country TEXT, city TEXT,
  bio TEXT, phone TEXT, avatar_url TEXT
);
CREATE TABLE musics (
  id TEXT PRIMARY KEY, title TEXT, artist TEXT, album TEXT, duration INTEGER,
  genre TEXT, label TEXT, composer TEXT, lyrics_snippet TEXT, cover_url TEXT
);
CREATE TABLE playlists (
  id TEXT PRIMARY KEY, user_id TEXT, name TEXT, description TEXT,
  genre_tags TEXT, mood TEXT, cover_url TEXT, notes TEXT
);
CREATE TABLE playlist_music (playlist_id TEXT, music_id TEXT);
"""


@strawberry.type
class User:
    id: str
    name: str
    email: str
    country: str
    city: str
    bio: str
    phone: str
    avatar_url: str


@strawberry.type
class Music:
    id: str
    title: str
    artist: str
    album: str
    duration: int
    genre: str
    label: str
    composer: str
    lyrics_snippet: str
    cover_url: str


@strawberry.type
class Playlist:
    id: str
    user_id: str
    name: str
    description: str
    genre_tags: str
    mood: str
    cover_url: str
    notes: str


def to_user(r):
    return User(
        id=r["id"], name=r["name"], email=r["email"], country=r["country"], city=r["city"],
        bio=r["bio"], phone=r["phone"], avatar_url=r["avatar_url"],
    )


def to_music(r):
    return Music(
        id=r["id"], title=r["title"], artist=r["artist"], album=r["album"], duration=r["duration"],
        genre=r["genre"], label=r["label"], composer=r["composer"],
        lyrics_snippet=r["lyrics_snippet"], cover_url=r["cover_url"],
    )


def to_playlist(r):
    return Playlist(
        id=r["id"], user_id=r["user_id"], name=r["name"], description=r["description"],
        genre_tags=r["genre_tags"], mood=r["mood"], cover_url=r["cover_url"], notes=r["notes"],
    )


def run_seed():
    data = build_seed_data()
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO users (id, name, email, country, city, bio, phone, avatar_url) "
        "VALUES (:id, :name, :email, :country, :city, :bio, :phone, :avatar_url)",
        data["users"],
    )
    conn.executemany(
        "INSERT INTO musics (id, title, artist, album, duration, genre, label, composer, "
        "lyrics_snippet, cover_url) VALUES (:id, :title, :artist, :album, :duration, :genre, "
        ":label, :composer, :lyrics_snippet, :cover_url)",
        data["musics"],
    )
    conn.executemany(
        "INSERT INTO playlists (id, user_id, name, description, genre_tags, mood, cover_url, notes) "
        "VALUES (:id, :user_id, :name, :description, :genre_tags, :mood, :cover_url, :notes)",
        data["playlists"],
    )
    conn.executemany(
        "INSERT INTO playlist_music VALUES (?, ?)",
        data["playlist_musics"],
    )
    conn.commit()
    return "seeded"


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return [to_user(r) for r in conn.execute("SELECT * FROM users").fetchall()]

    @strawberry.field
    def musics(self) -> List[Music]:
        return [to_music(r) for r in conn.execute("SELECT * FROM musics").fetchall()]

    @strawberry.field
    def playlists(self) -> List[Playlist]:
        return [to_playlist(r) for r in conn.execute("SELECT * FROM playlists").fetchall()]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def seed(self) -> str:
        return run_seed()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

run_seed()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
