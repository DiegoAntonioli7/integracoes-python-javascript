from http.server import HTTPServer, BaseHTTPRequestHandler
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, Column, String, Integer as SAInteger, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session

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


class MusicRow(Base):
    __tablename__ = "musics"
    id = Column(String, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(SAInteger)


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


def wrap_envelope(operation, inner_xml):
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<soapenv:Envelope xmlns:soapenv="{SOAPENV}" xmlns:tns="{NS}">'
        f"<soapenv:Body>"
        f"<tns:{operation}Response>{inner_xml}</tns:{operation}Response>"
        f"</soapenv:Body>"
        f"</soapenv:Envelope>"
    )


def handle_seed():
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
    return wrap_envelope("Seed", "<tns:result>seeded</tns:result>")


def handle_get_users():
    with Session(engine) as session:
        rows = session.query(UserRow).all()
        items = "".join(
            f"<tns:item><tns:id>{r.id}</tns:id><tns:name>{r.name}</tns:name><tns:email>{r.email}</tns:email></tns:item>"
            for r in rows
        )
    return wrap_envelope("GetUsers", items)


def handle_get_musics():
    with Session(engine) as session:
        rows = session.query(MusicRow).all()
        items = "".join(
            f"<tns:item><tns:id>{r.id}</tns:id><tns:title>{r.title}</tns:title>"
            f"<tns:artist>{r.artist}</tns:artist><tns:album>{r.album}</tns:album>"
            f"<tns:duration>{r.duration}</tns:duration></tns:item>"
            for r in rows
        )
    return wrap_envelope("GetMusics", items)


def handle_get_playlists():
    with Session(engine) as session:
        rows = session.query(PlaylistRow).all()
        items = "".join(
            f"<tns:item><tns:id>{r.id}</tns:id><tns:user_id>{r.user_id}</tns:user_id>"
            f"<tns:name>{r.name}</tns:name><tns:description>{r.description}</tns:description></tns:item>"
            for r in rows
        )
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

        # Resolve operation from SOAPAction header first, then fall back to XML body
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
