import sys
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'rest_python.db'}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class UserRow(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    bio = Column(String)
    phone = Column(String)
    avatar_url = Column(String)


class MusicRow(Base):
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


class PlaylistRow(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    genre_tags = Column(String)
    mood = Column(String)
    cover_url = Column(String)
    notes = Column(String)


playlist_music = Table(
    "playlist_music",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id")),
    Column("music_id", String, ForeignKey("musics.id")),
)

Base.metadata.create_all(engine)

app = FastAPI()


@app.post("/seed")
def seed():
    data = build_seed_data()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for u in data["users"]:
            session.add(UserRow(**u))
        for m in data["musics"]:
            session.add(MusicRow(**m))
        for p in data["playlists"]:
            session.add(PlaylistRow(**p))
        session.commit()
        for pl_id, m_id in data["playlist_musics"]:
            session.execute(
                playlist_music.insert().values(playlist_id=pl_id, music_id=m_id)
            )
        session.commit()
    return {"status": "seeded", "counts": {k: len(v) for k, v in data.items()}}


@app.get("/users")
def get_users():
    with Session(engine) as session:
        return [
            {
                "id": r.id, "name": r.name, "email": r.email,
                "country": r.country, "city": r.city, "bio": r.bio,
                "phone": r.phone, "avatar_url": r.avatar_url,
            }
            for r in session.query(UserRow).all()
        ]


@app.get("/musics")
def get_musics():
    with Session(engine) as session:
        return [
            {
                "id": r.id, "title": r.title, "artist": r.artist,
                "album": r.album, "duration": r.duration, "genre": r.genre,
                "label": r.label, "composer": r.composer,
                "lyrics_snippet": r.lyrics_snippet, "cover_url": r.cover_url,
            }
            for r in session.query(MusicRow).all()
        ]


@app.get("/playlists")
def get_playlists():
    with Session(engine) as session:
        return [
            {
                "id": r.id, "user_id": r.user_id, "name": r.name,
                "description": r.description, "genre_tags": r.genre_tags,
                "mood": r.mood, "cover_url": r.cover_url, "notes": r.notes,
            }
            for r in session.query(PlaylistRow).all()
        ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
