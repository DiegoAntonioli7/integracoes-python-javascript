import json
import sqlite3
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import Response

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DB_PATH = Path(__file__).parent / "rest_python.db"
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

app = FastAPI()


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
    return {
        "status": "seeded",
        "counts": {k: len(v) for k, v in data.items()},
    }


@app.post("/seed")
def seed():
    return run_seed()


@app.get("/users")
async def get_users():
    rows = [dict(r) for r in conn.execute("SELECT * FROM users").fetchall()]
    return Response(content=json.dumps(rows), media_type="application/json")


@app.get("/musics")
async def get_musics():
    rows = [dict(r) for r in conn.execute("SELECT * FROM musics").fetchall()]
    return Response(content=json.dumps(rows), media_type="application/json")


@app.get("/playlists")
async def get_playlists():
    rows = [dict(r) for r in conn.execute("SELECT * FROM playlists").fetchall()]
    return Response(content=json.dumps(rows), media_type="application/json")


run_seed()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
