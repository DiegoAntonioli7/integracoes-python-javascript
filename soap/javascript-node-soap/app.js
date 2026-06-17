const express = require('express');
const Database = require('better-sqlite3');
const { buildSeedData } = require('../../shared/seed_data');

const db = new Database('./soap_javascript.db');
const app = express();
const NS = 'http://streaming.api.com/v1';

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

function soapResponse(operation, innerContent) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="${NS}">
  <soapenv:Body>
    <tns:${operation}Response>${innerContent}</tns:${operation}Response>
  </soapenv:Body>
</soapenv:Envelope>`;
}

function userXml(u) {
  return (
    `<tns:item><tns:id>${u.id}</tns:id><tns:name>${u.name}</tns:name>`
    + `<tns:email>${u.email}</tns:email><tns:country>${u.country}</tns:country>`
    + `<tns:city>${u.city}</tns:city><tns:bio>${u.bio}</tns:bio>`
    + `<tns:phone>${u.phone}</tns:phone><tns:avatar_url>${u.avatar_url}</tns:avatar_url></tns:item>`
  );
}

function musicXml(m) {
  return (
    `<tns:item><tns:id>${m.id}</tns:id><tns:title>${m.title}</tns:title>`
    + `<tns:artist>${m.artist}</tns:artist><tns:album>${m.album}</tns:album>`
    + `<tns:duration>${m.duration}</tns:duration><tns:genre>${m.genre}</tns:genre>`
    + `<tns:label>${m.label}</tns:label><tns:composer>${m.composer}</tns:composer>`
    + `<tns:lyrics_snippet>${m.lyrics_snippet}</tns:lyrics_snippet>`
    + `<tns:cover_url>${m.cover_url}</tns:cover_url></tns:item>`
  );
}

function playlistXml(p) {
  return (
    `<tns:item><tns:id>${p.id}</tns:id><tns:user_id>${p.user_id}</tns:user_id>`
    + `<tns:name>${p.name}</tns:name><tns:description>${p.description}</tns:description>`
    + `<tns:genre_tags>${p.genre_tags}</tns:genre_tags><tns:mood>${p.mood}</tns:mood>`
    + `<tns:cover_url>${p.cover_url}</tns:cover_url><tns:notes>${p.notes}</tns:notes></tns:item>`
  );
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
    return res.send(soapResponse('Seed', '<tns:result>seeded</tns:result>'));
  }

  if (operation === 'GetUsers') {
    const users = db.prepare('SELECT * FROM users').all();
    const items = users.map(userXml).join('');
    return res.send(soapResponse('GetUsers', items));
  }

  if (operation === 'GetMusics') {
    const musics = db.prepare('SELECT * FROM musics').all();
    const items = musics.map(musicXml).join('');
    return res.send(soapResponse('GetMusics', items));
  }

  if (operation === 'GetPlaylists') {
    const playlists = db.prepare('SELECT * FROM playlists').all();
    const items = playlists.map(playlistXml).join('');
    return res.send(soapResponse('GetPlaylists', items));
  }

  res.status(400).send(soapResponse('Fault', '<tns:faultstring>Unknown operation</tns:faultstring>'));
});

runSeed();

app.listen(3002, () => console.log('SOAP JS running on port 3002'));
