const express = require('express');
const Database = require('better-sqlite3');

const db = new Database('./soap_javascript.db');
const app = express();
app.use(express.text({ type: '*/xml' }));
app.use(express.text({ type: 'text/xml' }));
app.use(express.text({ type: 'application/soap+xml' }));

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
const SEED_PLAYLIST_MUSICS = [['playlist-001', 'music-001'], ['playlist-001', 'music-002'], ['playlist-001', 'music-003']];

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

app.post('/', (req, res) => {
  const action = req.headers['soapaction'] || req.headers['SOAPAction'] || '';
  const operation = detectOperation(req.body, action);
  res.set('Content-Type', 'text/xml');

  if (operation === 'Seed') {
    db.exec('DELETE FROM playlist_music; DELETE FROM playlists; DELETE FROM musics; DELETE FROM users;');
    const insertUser = db.prepare('INSERT INTO users VALUES (@id, @name, @email)');
    const insertMusic = db.prepare('INSERT INTO musics VALUES (@id, @title, @artist, @album, @duration)');
    const insertPlaylist = db.prepare('INSERT INTO playlists VALUES (@id, @user_id, @name, @description)');
    const insertPM = db.prepare('INSERT INTO playlist_music VALUES (?, ?)');
    SEED_USERS.forEach(u => insertUser.run(u));
    SEED_MUSICS.forEach(m => insertMusic.run(m));
    SEED_PLAYLISTS.forEach(p => insertPlaylist.run(p));
    SEED_PLAYLIST_MUSICS.forEach(([pl, mu]) => insertPM.run(pl, mu));
    return res.send(soapResponse('<SeedResponse><result>seeded</result></SeedResponse>'));
  }

  if (operation === 'GetUsers') {
    const users = db.prepare('SELECT * FROM users').all();
    const items = users.map(u => `<user><id>${u.id}</id><name>${u.name}</name><email>${u.email}</email></user>`).join('');
    return res.send(soapResponse(`<GetUsersResponse>${items}</GetUsersResponse>`));
  }

  if (operation === 'GetMusics') {
    const musics = db.prepare('SELECT * FROM musics').all();
    const items = musics.map(m => `<music><id>${m.id}</id><title>${m.title}</title><artist>${m.artist}</artist><album>${m.album}</album><duration>${m.duration}</duration></music>`).join('');
    return res.send(soapResponse(`<GetMusicsResponse>${items}</GetMusicsResponse>`));
  }

  if (operation === 'GetPlaylists') {
    const playlists = db.prepare('SELECT * FROM playlists').all();
    const items = playlists.map(p => `<playlist><id>${p.id}</id><user_id>${p.user_id}</user_id><name>${p.name}</name><description>${p.description}</description></playlist>`).join('');
    return res.send(soapResponse(`<GetPlaylistsResponse>${items}</GetPlaylistsResponse>`));
  }

  res.status(400).send(soapResponse('<Fault><faultstring>Unknown operation</faultstring></Fault>'));
});

app.listen(3002, () => console.log('SOAP JS running on port 3002'));
