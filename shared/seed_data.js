const NUM_USERS = 200;
const NUM_MUSICS = 500;
const NUM_PLAYLISTS = 300;
const MUSICS_PER_PLAYLIST = 10;

function pad(value, width = 80) {
  return (value.repeat(Math.ceil(width / value.length))).slice(0, width);
}

function generateUsers() {
  return Array.from({ length: NUM_USERS }, (_, idx) => {
    const i = idx + 1;
    return {
      id: `user-${String(i).padStart(4, '0')}`,
      name: `User ${i}`,
      email: `user${i}@streaming.example.com`,
      country: `Country ${i % 50}`,
      city: `City ${i % 100}`,
      bio: pad(`Bio for user ${i}: profile description used in load testing. `),
      phone: `+55 85 9${String(i % 10000).padStart(4, '0')}-${String(i % 10000).padStart(4, '0')}`,
      avatar_url: `https://cdn.streaming.example.com/avatars/user-${String(i).padStart(4, '0')}.jpg`,
    };
  });
}

function generateMusics() {
  const genres = ['Pop', 'Rock', 'Jazz', 'Classical', 'Electronic', 'Hip-Hop', 'Samba', 'MPB'];
  return Array.from({ length: NUM_MUSICS }, (_, idx) => {
    const i = idx + 1;
    return {
      id: `music-${String(i).padStart(4, '0')}`,
      title: `Song Title ${i}`,
      artist: `Artist ${i % 120}`,
      album: `Album ${i % 80}`,
      duration: 180 + (i % 240),
      genre: genres[i % genres.length],
      label: `Record Label ${i % 40}`,
      composer: `Composer ${i % 60}`,
      lyrics_snippet: pad(`Lyrics snippet for track ${i}: verse and chorus text for payload size. `),
      cover_url: `https://cdn.streaming.example.com/covers/music-${String(i).padStart(4, '0')}.jpg`,
    };
  });
}

function generatePlaylists() {
  const moods = ['Chill', 'Focus', 'Workout', 'Party', 'Sleep', 'Road Trip', 'Study', 'Romance'];
  return Array.from({ length: NUM_PLAYLISTS }, (_, idx) => {
    const i = idx + 1;
    return {
      id: `playlist-${String(i).padStart(4, '0')}`,
      user_id: `user-${String((i % NUM_USERS) + 1).padStart(4, '0')}`,
      name: `Playlist ${i}`,
      description: pad(`Description for playlist ${i} with curated tracks for load testing. `),
      genre_tags: `${moods[i % moods.length]}, ${moods[(i + 3) % moods.length]}`,
      mood: moods[i % moods.length],
      cover_url: `https://cdn.streaming.example.com/playlists/playlist-${String(i).padStart(4, '0')}.jpg`,
      notes: pad(`Editor notes for playlist ${i}: sequencing and transitions for benchmark payloads. `),
    };
  });
}

function generatePlaylistMusics() {
  const links = [];
  for (let i = 1; i <= NUM_PLAYLISTS; i += 1) {
    const playlistId = `playlist-${String(i).padStart(4, '0')}`;
    for (let j = 0; j < MUSICS_PER_PLAYLIST; j += 1) {
      const musicIndex = ((i - 1) * MUSICS_PER_PLAYLIST + j) % NUM_MUSICS + 1;
      links.push([playlistId, `music-${String(musicIndex).padStart(4, '0')}`]);
    }
  }
  return links;
}

function buildSeedData() {
  return {
    users: generateUsers(),
    musics: generateMusics(),
    playlists: generatePlaylists(),
    playlistMusics: generatePlaylistMusics(),
  };
}

module.exports = {
  NUM_USERS,
  NUM_MUSICS,
  NUM_PLAYLISTS,
  buildSeedData,
};
