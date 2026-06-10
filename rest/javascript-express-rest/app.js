const express = require('express');
const Database = require('better-sqlite3');
const { buildSeedData } = require('../../shared/seed_data');

const db = new Database('./rest_javascript.db');
const app = express();
app.use(express.json());

function recreateSchema() {
  db.exec(`
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
  `);
}

recreateSchema();

function runSeed() {
  recreateSchema();
  const data = buildSeedData();
  const insertUser = db.prepare(`
    INSERT INTO users (id, name, email, country, city, bio, phone, avatar_url)
    VALUES (@id, @name, @email, @country, @city, @bio, @phone, @avatar_url)
  `);
  const insertMusic = db.prepare(`
    INSERT INTO musics (id, title, artist, album, duration, genre, label, composer, lyrics_snippet, cover_url)
    VALUES (@id, @title, @artist, @album, @duration, @genre, @label, @composer, @lyrics_snippet, @cover_url)
  `);
  const insertPlaylist = db.prepare(`
    INSERT INTO playlists (id, user_id, name, description, genre_tags, mood, cover_url, notes)
    VALUES (@id, @user_id, @name, @description, @genre_tags, @mood, @cover_url, @notes)
  `);
  const insertPM = db.prepare('INSERT INTO playlist_music VALUES (?, ?)');

  data.users.forEach((u) => insertUser.run(u));
  data.musics.forEach((m) => insertMusic.run(m));
  data.playlists.forEach((p) => insertPlaylist.run(p));
  data.playlistMusics.forEach(([pl, mu]) => insertPM.run(pl, mu));

  return {
    status: 'seeded',
    counts: {
      users: data.users.length,
      musics: data.musics.length,
      playlists: data.playlists.length,
      playlist_musics: data.playlistMusics.length,
    },
  };
}

app.post('/seed', (req, res) => {
  res.json(runSeed());
});

app.get('/users', (req, res) => {
  res.json(db.prepare('SELECT * FROM users').all());
});

app.get('/musics', (req, res) => {
  res.json(db.prepare('SELECT * FROM musics').all());
});

app.get('/playlists', (req, res) => {
  res.json(db.prepare('SELECT * FROM playlists').all());
});

app.listen(3001, () => console.log('REST JS running on port 3001'));
