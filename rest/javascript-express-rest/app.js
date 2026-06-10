const express = require('express');
const Database = require('better-sqlite3');

const db = new Database('./rest_javascript.db');
const app = express();
app.use(express.json());

db.exec(`
  CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT, email TEXT);
  CREATE TABLE IF NOT EXISTS musics (id TEXT PRIMARY KEY, title TEXT, artist TEXT, album TEXT, duration INTEGER);
  CREATE TABLE IF NOT EXISTS playlists (id TEXT PRIMARY KEY, user_id TEXT, name TEXT, description TEXT);
  CREATE TABLE IF NOT EXISTS playlist_music (playlist_id TEXT, music_id TEXT);
`);

const SEED_USERS = [{ id: 'user-001', name: 'Test User', email: 'test@test.com' }];
const SEED_MUSICS = [
  { id: 'music-001', title: 'Song 1', artist: 'Artist 1', album: 'Album 1', duration: 200 },
  { id: 'music-002', title: 'Song 2', artist: 'Artist 2', album: 'Album 2', duration: 210 },
  { id: 'music-003', title: 'Song 3', artist: 'Artist 3', album: 'Album 3', duration: 220 },
];
const SEED_PLAYLISTS = [{ id: 'playlist-001', user_id: 'user-001', name: 'Test Playlist', description: 'Load test' }];
const SEED_PLAYLIST_MUSICS = [
  ['playlist-001', 'music-001'],
  ['playlist-001', 'music-002'],
  ['playlist-001', 'music-003'],
];

app.post('/seed', (req, res) => {
  db.exec('DELETE FROM playlist_music; DELETE FROM playlists; DELETE FROM musics; DELETE FROM users;');
  const insertUser = db.prepare('INSERT INTO users VALUES (@id, @name, @email)');
  const insertMusic = db.prepare('INSERT INTO musics VALUES (@id, @title, @artist, @album, @duration)');
  const insertPlaylist = db.prepare('INSERT INTO playlists VALUES (@id, @user_id, @name, @description)');
  const insertPM = db.prepare('INSERT INTO playlist_music VALUES (?, ?)');
  SEED_USERS.forEach(u => insertUser.run(u));
  SEED_MUSICS.forEach(m => insertMusic.run(m));
  SEED_PLAYLISTS.forEach(p => insertPlaylist.run(p));
  SEED_PLAYLIST_MUSICS.forEach(([pl, mu]) => insertPM.run(pl, mu));
  res.json({ status: 'seeded' });
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
