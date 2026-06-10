import sys
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DATABASE_URL = "sqlite:///./rest_python.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

app = FastAPI()


class Base(DeclarativeBase):
    pass


playlist_music = Table(
    "playlist_music",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id")),
    Column("music_id", String, ForeignKey("musics.id")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    bio = Column(String)
    phone = Column(String)
    avatar_url = Column(String)


class Music(Base):
    __tablename__ = "musics"
    id = Column(String, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(Integer)
    genre = Column(String)
    label = Column(String)
    composer = Column(String)
    lyrics_snippet = Column(String)
    cover_url = Column(String)


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    genre_tags = Column(String)
    mood = Column(String)
    cover_url = Column(String)
    notes = Column(String)


Base.metadata.create_all(engine)


def user_dict(u):
    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "country": u.country,
        "city": u.city,
        "bio": u.bio,
        "phone": u.phone,
        "avatar_url": u.avatar_url,
    }


def music_dict(m):
    return {
        "id": m.id,
        "title": m.title,
        "artist": m.artist,
        "album": m.album,
        "duration": m.duration,
        "genre": m.genre,
        "label": m.label,
        "composer": m.composer,
        "lyrics_snippet": m.lyrics_snippet,
        "cover_url": m.cover_url,
    }


def playlist_dict(p):
    return {
        "id": p.id,
        "user_id": p.user_id,
        "name": p.name,
        "description": p.description,
        "genre_tags": p.genre_tags,
        "mood": p.mood,
        "cover_url": p.cover_url,
        "notes": p.notes,
    }


@app.post("/seed")
def seed():
    data = build_seed_data()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for u in data["users"]:
            session.add(User(**u))
        for m in data["musics"]:
            session.add(Music(**m))
        for p in data["playlists"]:
            session.add(Playlist(**p))
        session.commit()
        for pl_id, m_id in data["playlist_musics"]:
            session.execute(playlist_music.insert().values(playlist_id=pl_id, music_id=m_id))
        session.commit()
    return {"status": "seeded", "counts": {k: len(v) for k, v in data.items()}}


@app.get("/users")
def get_users():
    with Session(engine) as session:
        return [user_dict(u) for u in session.query(User).all()]


@app.get("/musics")
def get_musics():
    with Session(engine) as session:
        return [music_dict(m) for m in session.query(Music).all()]


@app.get("/playlists")
def get_playlists():
    with Session(engine) as session:
        return [playlist_dict(p) for p in session.query(Playlist).all()]
