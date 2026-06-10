const express = require('express');
const Database = require('better-sqlite3');
const { buildSeedData } = require('../../shared/seed_data');

const db = new Database('./soap_javascript.db');
const app = express();
app.use(express.text({ type: '*/xml' }));
app.use(express.text({ type: 'text/xml' }));
app.use(express.text({ type: 'application/soap+xml' }));

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

function soapResponse(bodyContent) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>${bodyContent}</soapenv:Body>
</soapenv:Envelope>`;
}

function detectOperation(body, action) {
  const combined = (body || '') + (action || '');
  if (/Seed/i.test(combined)) return 'Seed';
  if (/GetUsers/i.test(combined)) return 'GetUsers';
  if (/GetMusics/i.test(combined)) return 'GetMusics';
  if (/GetPlaylists/i.test(combined)) return 'GetPlaylists';
  return null;
}

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
}

app.post('/', (req, res) => {
  const action = req.headers['soapaction'] || req.headers['SOAPAction'] || '';
  const operation = detectOperation(req.body, action);
  res.set('Content-Type', 'text/xml');

  if (operation === 'Seed') {
    runSeed();
    return res.send(soapResponse('<SeedResponse><result>seeded</result></SeedResponse>'));
  }

  if (operation === 'GetUsers') {
    const users = db.prepare('SELECT * FROM users').all();
    const items = users.map((u) => (
      `<user><id>${u.id}</id><name>${u.name}</name><email>${u.email}</email>`
      + `<country>${u.country}</country><city>${u.city}</city><bio>${u.bio}</bio>`
      + `<phone>${u.phone}</phone><avatar_url>${u.avatar_url}</avatar_url></user>`
    )).join('');
    return res.send(soapResponse(`<GetUsersResponse>${items}</GetUsersResponse>`));
  }

  if (operation === 'GetMusics') {
    const musics = db.prepare('SELECT * FROM musics').all();
    const items = musics.map((m) => (
      `<music><id>${m.id}</id><title>${m.title}</title><artist>${m.artist}</artist>`
      + `<album>${m.album}</album><duration>${m.duration}</duration><genre>${m.genre}</genre>`
      + `<label>${m.label}</label><composer>${m.composer}</composer>`
      + `<lyrics_snippet>${m.lyrics_snippet}</lyrics_snippet><cover_url>${m.cover_url}</cover_url></music>`
    )).join('');
    return res.send(soapResponse(`<GetMusicsResponse>${items}</GetMusicsResponse>`));
  }

  if (operation === 'GetPlaylists') {
    const playlists = db.prepare('SELECT * FROM playlists').all();
    const items = playlists.map((p) => (
      `<playlist><id>${p.id}</id><user_id>${p.user_id}</user_id><name>${p.name}</name>`
      + `<description>${p.description}</description><genre_tags>${p.genre_tags}</genre_tags>`
      + `<mood>${p.mood}</mood><cover_url>${p.cover_url}</cover_url><notes>${p.notes}</notes></playlist>`
    )).join('');
    return res.send(soapResponse(`<GetPlaylistsResponse>${items}</GetPlaylistsResponse>`));
  }

  res.status(400).send(soapResponse('<Fault><faultstring>Unknown operation</faultstring></Fault>'));
});

app.listen(3002, () => console.log('SOAP JS running on port 3002'));
