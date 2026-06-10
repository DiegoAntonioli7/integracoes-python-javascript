import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, Column, String, Integer as SAInteger, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DATABASE_URL = "sqlite:///./soap_python.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

NS = "http://streaming.api.com/v1"
SOAPENV = "http://schemas.xmlsoap.org/soap/envelope/"


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
    duration = Column(SAInteger)
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


def wrap_envelope(operation, inner_xml):
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<soapenv:Envelope xmlns:soapenv="{SOAPENV}" xmlns:tns="{NS}">'
        f"<soapenv:Body>"
        f"<tns:{operation}Response>{inner_xml}</tns:{operation}Response>"
        f"</soapenv:Body>"
        f"</soapenv:Envelope>"
    )


def user_xml(r):
    return (
        f"<tns:item><tns:id>{r.id}</tns:id><tns:name>{r.name}</tns:name>"
        f"<tns:email>{r.email}</tns:email><tns:country>{r.country}</tns:country>"
        f"<tns:city>{r.city}</tns:city><tns:bio>{r.bio}</tns:bio>"
        f"<tns:phone>{r.phone}</tns:phone><tns:avatar_url>{r.avatar_url}</tns:avatar_url></tns:item>"
    )


def music_xml(r):
    return (
        f"<tns:item><tns:id>{r.id}</tns:id><tns:title>{r.title}</tns:title>"
        f"<tns:artist>{r.artist}</tns:artist><tns:album>{r.album}</tns:album>"
        f"<tns:duration>{r.duration}</tns:duration><tns:genre>{r.genre}</tns:genre>"
        f"<tns:label>{r.label}</tns:label><tns:composer>{r.composer}</tns:composer>"
        f"<tns:lyrics_snippet>{r.lyrics_snippet}</tns:lyrics_snippet>"
        f"<tns:cover_url>{r.cover_url}</tns:cover_url></tns:item>"
    )


def playlist_xml(r):
    return (
        f"<tns:item><tns:id>{r.id}</tns:id><tns:user_id>{r.user_id}</tns:user_id>"
        f"<tns:name>{r.name}</tns:name><tns:description>{r.description}</tns:description>"
        f"<tns:genre_tags>{r.genre_tags}</tns:genre_tags><tns:mood>{r.mood}</tns:mood>"
        f"<tns:cover_url>{r.cover_url}</tns:cover_url><tns:notes>{r.notes}</tns:notes></tns:item>"
    )


def handle_seed():
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
    return wrap_envelope("Seed", "<tns:result>seeded</tns:result>")


def handle_get_users():
    with Session(engine) as session:
        items = "".join(user_xml(r) for r in session.query(UserRow).all())
    return wrap_envelope("GetUsers", items)


def handle_get_musics():
    with Session(engine) as session:
        items = "".join(music_xml(r) for r in session.query(MusicRow).all())
    return wrap_envelope("GetMusics", items)


def handle_get_playlists():
    with Session(engine) as session:
        items = "".join(playlist_xml(r) for r in session.query(PlaylistRow).all())
    return wrap_envelope("GetPlaylists", items)


HANDLERS = {
    "Seed": handle_seed,
    "GetUsers": handle_get_users,
    "GetMusics": handle_get_musics,
    "GetPlaylists": handle_get_playlists,
}


class SOAPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        soap_action = self.headers.get("SOAPAction", "").strip('"')
        operation = soap_action.split("#")[-1] if "#" in soap_action else None

        if not operation:
            try:
                root = ET.fromstring(body)
                body_elem = root.find(f"{{{SOAPENV}}}Body")
                if body_elem is not None:
                    for child in body_elem:
                        tag = child.tag
                        operation = tag.split("}")[1] if "}" in tag else tag
                        break
            except ET.ParseError:
                pass

        handler = HANDLERS.get(operation)
        if handler is None:
            self.send_response(400)
            self.end_headers()
            return

        response = handler()
        encoded = response.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8001), SOAPHandler)
    print("SOAP Python running on port 8001")
    server.serve_forever()
