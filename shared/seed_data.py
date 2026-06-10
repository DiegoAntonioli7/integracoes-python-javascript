NUM_USERS = 200
NUM_MUSICS = 500
NUM_PLAYLISTS = 300
MUSICS_PER_PLAYLIST = 10


def _pad(value: str, width: int = 80) -> str:
    return (value * ((width // len(value)) + 1))[:width]


def generate_users():
    return [
        {
            "id": f"user-{i:04d}",
            "name": f"User {i}",
            "email": f"user{i}@streaming.example.com",
            "country": f"Country {i % 50}",
            "city": f"City {i % 100}",
            "bio": _pad(f"Bio for user {i}: profile description used in load testing. "),
            "phone": f"+55 85 9{i % 10000:04d}-{i % 10000:04d}",
            "avatar_url": f"https://cdn.streaming.example.com/avatars/user-{i:04d}.jpg",
        }
        for i in range(1, NUM_USERS + 1)
    ]


def generate_musics():
    genres = ("Pop", "Rock", "Jazz", "Classical", "Electronic", "Hip-Hop", "Samba", "MPB")
    return [
        {
            "id": f"music-{i:04d}",
            "title": f"Song Title {i}",
            "artist": f"Artist {i % 120}",
            "album": f"Album {i % 80}",
            "duration": 180 + (i % 240),
            "genre": genres[i % len(genres)],
            "label": f"Record Label {i % 40}",
            "composer": f"Composer {i % 60}",
            "lyrics_snippet": _pad(f"Lyrics snippet for track {i}: verse and chorus text for payload size. "),
            "cover_url": f"https://cdn.streaming.example.com/covers/music-{i:04d}.jpg",
        }
        for i in range(1, NUM_MUSICS + 1)
    ]


def generate_playlists():
    moods = ("Chill", "Focus", "Workout", "Party", "Sleep", "Road Trip", "Study", "Romance")
    return [
        {
            "id": f"playlist-{i:04d}",
            "user_id": f"user-{(i % NUM_USERS) + 1:04d}",
            "name": f"Playlist {i}",
            "description": _pad(f"Description for playlist {i} with curated tracks for load testing. "),
            "genre_tags": f"{moods[i % len(moods)]}, {moods[(i + 3) % len(moods)]}",
            "mood": moods[i % len(moods)],
            "cover_url": f"https://cdn.streaming.example.com/playlists/playlist-{i:04d}.jpg",
            "notes": _pad(f"Editor notes for playlist {i}: sequencing and transitions for benchmark payloads. "),
        }
        for i in range(1, NUM_PLAYLISTS + 1)
    ]


def generate_playlist_musics():
    links = []
    for i in range(1, NUM_PLAYLISTS + 1):
        playlist_id = f"playlist-{i:04d}"
        for j in range(MUSICS_PER_PLAYLIST):
            music_id = f"music-{((i - 1) * MUSICS_PER_PLAYLIST + j) % NUM_MUSICS + 1:04d}"
            links.append((playlist_id, music_id))
    return links


def build_seed_data():
    return {
        "users": generate_users(),
        "musics": generate_musics(),
        "playlists": generate_playlists(),
        "playlist_musics": generate_playlist_musics(),
    }
