import sqlite3
import sys
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from shared.seed_data import build_seed_data

DB_PATH = Path(__file__).parent / "soap_python.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row

NS = "http://streaming.api.com/v1"
SOAPENV = "http://schemas.xmlsoap.org/soap/envelope/"

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
        f"<tns:item><tns:id>{r['id']}</tns:id><tns:name>{r['name']}</tns:name>"
        f"<tns:email>{r['email']}</tns:email><tns:country>{r['country']}</tns:country>"
        f"<tns:city>{r['city']}</tns:city><tns:bio>{r['bio']}</tns:bio>"
        f"<tns:phone>{r['phone']}</tns:phone><tns:avatar_url>{r['avatar_url']}</tns:avatar_url></tns:item>"
    )


def music_xml(r):
    return (
        f"<tns:item><tns:id>{r['id']}</tns:id><tns:title>{r['title']}</tns:title>"
        f"<tns:artist>{r['artist']}</tns:artist><tns:album>{r['album']}</tns:album>"
        f"<tns:duration>{r['duration']}</tns:duration><tns:genre>{r['genre']}</tns:genre>"
        f"<tns:label>{r['label']}</tns:label><tns:composer>{r['composer']}</tns:composer>"
        f"<tns:lyrics_snippet>{r['lyrics_snippet']}</tns:lyrics_snippet>"
        f"<tns:cover_url>{r['cover_url']}</tns:cover_url></tns:item>"
    )


def playlist_xml(r):
    return (
        f"<tns:item><tns:id>{r['id']}</tns:id><tns:user_id>{r['user_id']}</tns:user_id>"
        f"<tns:name>{r['name']}</tns:name><tns:description>{r['description']}</tns:description>"
        f"<tns:genre_tags>{r['genre_tags']}</tns:genre_tags><tns:mood>{r['mood']}</tns:mood>"
        f"<tns:cover_url>{r['cover_url']}</tns:cover_url><tns:notes>{r['notes']}</tns:notes></tns:item>"
    )


def handle_seed():
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
    return wrap_envelope("Seed", "<tns:result>seeded</tns:result>")


def handle_get_users():
    items = "".join(user_xml(r) for r in conn.execute("SELECT * FROM users").fetchall())
    return wrap_envelope("GetUsers", items)


def handle_get_musics():
    items = "".join(music_xml(r) for r in conn.execute("SELECT * FROM musics").fetchall())
    return wrap_envelope("GetMusics", items)


def handle_get_playlists():
    items = "".join(playlist_xml(r) for r in conn.execute("SELECT * FROM playlists").fetchall())
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


handle_seed()

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8001), SOAPHandler)
    print("SOAP Python running on port 8001")
    server.serve_forever()
