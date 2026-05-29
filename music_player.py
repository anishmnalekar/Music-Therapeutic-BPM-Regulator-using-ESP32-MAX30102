# music_player.py
from dfplayer import DFPlayer
import time
try:
    import urandom as random  # MicroPython
except ImportError:
    import random

# Map genres to DFPlayer folders (1..99)
GENRE_FOLDER = {
    "calm": 1,
    "energetic": 2,
    "neutral": 3,
}

# === Set how many tracks exist in each folder ===
TRACK_COUNT = {
    "calm": 5,
    "energetic": 5,
    "neutral": 5,
}

AUTO_STOP_MS = 60_000  # 60 seconds

_dfp = None
_current_genre = None
_playlist = []
_playlist_idx = -1
_music_end_time = 0
_is_playing = False


def _init_player():
    global _dfp
    if _dfp is None:
        _dfp = DFPlayer()
        _dfp.volume(20)  # 0..30
        time.sleep_ms(200)


def _make_shuffled_tracks(count):
    arr = list(range(1, count + 1))
    for i in range(len(arr) - 1, 0, -1):
        r = random.getrandbits(30) if hasattr(random, "getrandbits") else int(random.random() * 0x3fffffff)
        j = r % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def _ensure_playlist_for_genre(genre):
    global _playlist, _playlist_idx, _current_genre
    if genre != _current_genre:
        _current_genre = genre
        count = TRACK_COUNT.get(genre, 1)
        _playlist = _make_shuffled_tracks(max(1, int(count)))
        _playlist_idx = -1


def _play_current_track():
    global _music_end_time, _is_playing, _playlist, _playlist_idx, _current_genre
    if not _playlist or _playlist_idx < 0:
        return
    folder = GENRE_FOLDER.get(_current_genre, 1)
    track = _playlist[_playlist_idx]
    _dfp.play_folder_track(folder, track)
    _music_end_time = time.ticks_add(time.ticks_ms(), AUTO_STOP_MS)
    _is_playing = True


def _advance_index_circular():
    global _playlist_idx, _playlist
    if not _playlist:
        return
    _playlist_idx += 1
    if _playlist_idx >= len(_playlist):
        _playlist = _make_shuffled_tracks(len(_playlist))
        _playlist_idx = 0


def start_music(genre):
    global _current_genre
    _init_player()
    _ensure_playlist_for_genre(genre)
    _advance_index_circular()
    _play_current_track()


def stop_music():
    global _is_playing
    if _dfp:
        _dfp.stop()
    _is_playing = False


def resume_music():
    global _playlist_idx, _current_genre
    _init_player()
    if _current_genre is None:
        start_music("calm")
        return
    if _playlist_idx < 0:
        _advance_index_circular()
    _play_current_track()


def next_music():
    global _current_genre
    _init_player()
    if _current_genre is None:
        start_music("calm")
        return
    _advance_index_circular()
    _play_current_track()


def check_auto_stop():
    global _is_playing
    if _is_playing and time.ticks_diff(time.ticks_ms(), _music_end_time) >= 0:
        stop_music()

