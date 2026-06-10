import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from typing import List

DATABASE_URL = "sqlite:///./graphql_python.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


playlist_music = Table(
    "playlist_music",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id")),
    Column("music_id", String, ForeignKey("musics.id")),
)


class UserRow(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)


class MusicRow(Base):
    __tablename__ = "musics"
    id = Column(String, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(Integer)


class PlaylistRow(Base):
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
SEED_PLAYLIST_MUSICS = [("playlist-001", "music-001"), ("playlist-001", "music-002"), ("playlist-001", "music-003")]


@strawberry.type
class User:
    id: str
    name: str
    email: str


@strawberry.type
class Music:
    id: str
    title: str
    artist: str
    album: str
    duration: int


@strawberry.type
class Playlist:
    id: str
    user_id: str
    name: str
    description: str


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        with Session(engine) as session:
            return [User(id=r.id, name=r.name, email=r.email) for r in session.query(UserRow).all()]

    @strawberry.field
    def musics(self) -> List[Music]:
        with Session(engine) as session:
            return [Music(id=r.id, title=r.title, artist=r.artist, album=r.album, duration=r.duration) for r in session.query(MusicRow).all()]

    @strawberry.field
    def playlists(self) -> List[Playlist]:
        with Session(engine) as session:
            return [Playlist(id=r.id, user_id=r.user_id, name=r.name, description=r.description) for r in session.query(PlaylistRow).all()]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def seed(self) -> str:
        with Session(engine) as session:
            session.execute(playlist_music.delete())
            session.query(PlaylistRow).delete()
            session.query(MusicRow).delete()
            session.query(UserRow).delete()
            for u in SEED_USERS:
                session.add(UserRow(**u))
            for m in SEED_MUSICS:
                session.add(MusicRow(**m))
            for p in SEED_PLAYLISTS:
                session.add(PlaylistRow(**p))
            session.commit()
            for pl_id, m_id in SEED_PLAYLIST_MUSICS:
                session.execute(playlist_music.insert().values(playlist_id=pl_id, music_id=m_id))
            session.commit()
        return "seeded"


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
