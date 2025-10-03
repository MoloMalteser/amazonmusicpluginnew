import sys
import os

# defaults-Ordner zum Pfad hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), "../defaults"))

from amazonmusic import AmazonMusic
from settings import SettingsManager
import subprocess
import logging

logger = logging.getLogger(__name__)

# Initialize SettingsManager
settingsDir = os.environ["DECKY_PLUGIN_SETTINGS_DIR"]
settings = SettingsManager(name="settings", settings_directory=settingsDir)
settings.read()

class Plugin:
    def __init__(self):
        self.am = None

    async def init_am(self, email: str, password: str):
        self.am = AmazonMusic(credentials=lambda: [email, password])
        return {"status": "initialized"}

    async def search_songs(self, query: str):
        results = []
        search_res = self.am.search(query, tracks=True, albums=False, playlists=False, artists=False, stations=False)
        for label, item in search_res:
            for doc in item.get("documents", []):
                results.append({
                    "title": doc.get("title"),
                    "artist": doc.get("artistName"),
                    "id": doc.get("asin")
                })
        return results

    async def recommendations(self):
        recs = []
        for album in self.am.albums:
            for track in album.tracks:
                recs.append({
                    "title": track.name,
                    "artist": track.artist,
                    "id": track.identifier
                })
                if len(recs) >= 6:
                    break
            if len(recs) >= 6:
                break
        return recs

    async def recently_played(self):
        return settings.getSetting("recent", [])

    async def play_song(self, song_id: str):
        for album in self.am.albums:
            for track in album.tracks:
                if track.identifier == song_id:
                    subprocess.run(["mpv", "--no-video", track.stream_url])
                    recent = settings.getSetting("recent", [])
                    recent.insert(0, {"title": track.name, "artist": track.artist, "id": track.identifier})
                    settings.setSetting("recent", recent[:6])
                    settings.commit()
                    return {"status": "playing", "track": track.name}
        return {"status": "not_found"}

    async def _main(self):
        pass

    async def _unload(self):
        pass
