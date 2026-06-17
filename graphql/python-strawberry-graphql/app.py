import sys
from pathlib import Path

import strawberry
from strawberry.schema.config import StrawberryConfig
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from typing import List

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

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


Base.metadata.create_all(engine)


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
        id=r.id, name=r.name, email=r.email, country=r.country, city=r.city,
        bio=r.bio, phone=r.phone, avatar_url=r.avatar_url,
    )


def to_music(r):
    return Music(
        id=r.id, title=r.title, artist=r.artist, album=r.album, duration=r.duration,
        genre=r.genre, label=r.label, composer=r.composer,
        lyrics_snippet=r.lyrics_snippet, cover_url=r.cover_url,
    )


def to_playlist(r):
    return Playlist(
        id=r.id, user_id=r.user_id, name=r.name, description=r.description,
        genre_tags=r.genre_tags, mood=r.mood, cover_url=r.cover_url, notes=r.notes,
    )


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        with Session(engine) as session:
            return [to_user(r) for r in session.query(UserRow).all()]

    @strawberry.field
    def musics(self) -> List[Music]:
        with Session(engine) as session:
            return [to_music(r) for r in session.query(MusicRow).all()]

    @strawberry.field
    def playlists(self) -> List[Playlist]:
        with Session(engine) as session:
            return [to_playlist(r) for r in session.query(PlaylistRow).all()]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def seed(self) -> str:
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
                session.execute(playlist_music.insert().values(playlist_id=pl_id, music_id=m_id))
            session.commit()
        return "seeded"


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
