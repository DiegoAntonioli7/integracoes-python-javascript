from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session

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


class Music(Base):
    __tablename__ = "musics"
    id = Column(String, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(Integer)


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)


Base.metadata.create_all(engine)

SEED_USERS = [{"id": "user-001", "name": "Test User", "email": "test@test.com"}]
SEED_MUSICS = [
    {"id": "music-001", "title": "Song 1", "artist": "Artist 1", "album": "Album 1", "duration": 200},
    {"id": "music-002", "title": "Song 2", "artist": "Artist 2", "album": "Album 2", "duration": 210},
    {"id": "music-003", "title": "Song 3", "artist": "Artist 3", "album": "Album 3", "duration": 220},
]
SEED_PLAYLISTS = [
    {"id": "playlist-001", "user_id": "user-001", "name": "Test Playlist", "description": "Load test"}
]
SEED_PLAYLIST_MUSICS = [
    ("playlist-001", "music-001"),
    ("playlist-001", "music-002"),
    ("playlist-001", "music-003"),
]


@app.post("/seed")
def seed():
    with Session(engine) as session:
        session.execute(playlist_music.delete())
        session.query(Playlist).delete()
        session.query(Music).delete()
        session.query(User).delete()
        for u in SEED_USERS:
            session.add(User(**u))
        for m in SEED_MUSICS:
            session.add(Music(**m))
        for p in SEED_PLAYLISTS:
            session.add(Playlist(**p))
        session.commit()
        for pl_id, m_id in SEED_PLAYLIST_MUSICS:
            session.execute(playlist_music.insert().values(playlist_id=pl_id, music_id=m_id))
        session.commit()
    return {"status": "seeded"}


@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@app.get("/musics")
def get_musics():
    with Session(engine) as session:
        musics = session.query(Music).all()
        return [{"id": m.id, "title": m.title, "artist": m.artist, "album": m.album, "duration": m.duration} for m in musics]


@app.get("/playlists")
def get_playlists():
    with Session(engine) as session:
        playlists = session.query(Playlist).all()
        return [{"id": p.id, "user_id": p.user_id, "name": p.name, "description": p.description} for p in playlists]
