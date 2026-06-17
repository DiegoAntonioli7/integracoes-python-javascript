const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const Database = require('better-sqlite3');
const { buildSeedData } = require('../../shared/seed_data');

const db = new Database('./graphql_javascript.db');

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

const typeDefs = `
  type User {
    id: ID!, name: String!, email: String!, country: String!, city: String!,
    bio: String!, phone: String!, avatar_url: String!
  }
  type Music {
    id: ID!, title: String!, artist: String!, album: String!, duration: Int!,
    genre: String!, label: String!, composer: String!, lyrics_snippet: String!, cover_url: String!
  }
  type Playlist {
    id: ID!, user_id: String!, name: String!, description: String!,
    genre_tags: String!, mood: String!, cover_url: String!, notes: String!
  }
  type Query {
    users: [User!]!
    musics: [Music!]!
    playlists: [Playlist!]!
  }
  type Mutation {
    seed: String!
  }
`;

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
  return 'seeded';
}

runSeed();

const stmts = {
  users: db.prepare('SELECT * FROM users'),
  musics: db.prepare('SELECT * FROM musics'),
  playlists: db.prepare('SELECT * FROM playlists'),
};

const resolvers = {
  Query: {
    users: () => stmts.users.all(),
    musics: () => stmts.musics.all(),
    playlists: () => stmts.playlists.all(),
  },
  Mutation: {
    seed: () => runSeed(),
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

startStandaloneServer(server, { listen: { port: 3003 } }).then(({ url }) => {
  console.log(`GraphQL JS running at ${url}`);
});
