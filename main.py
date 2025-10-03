import os
from amazonmusic import AmazonMusic
from settings import SettingsManager
import logging
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Settings-Pfad von Decky
settingsDir = os.environ["DECKY_PLUGIN_SETTINGS_DIR"]
settings = SettingsManager(name="settings", settings_directory=settingsDir)
settings.read()

# Funktion, um Amazon Music Client zu erstellen
def get_am_client():
    creds = settings.getSetting("credentials", None)
    if not creds:
        # Wenn keine Credentials gespeichert sind, Platzhalter leer lassen
        creds = ["", ""]
    return AmazonMusic(credentials=lambda: creds)

am = get_am_client()

class Plugin:
    async def set_credentials(self, email: str, password: str):
        settings.setSetting("credentials", [email, password])
        settings.commit()
        global am
        am = get_am_client()
        return {"status": "saved"}

    async def recommendations(self):
        station = am.create_station("A2UW0MECRAWILL")
        return [{"id": t.id, "title": t.name, "artist": t.artist} for t in station.tracks[:10]]

    async def recently_played(self):
        tracks = am.library.get("recently_played", [])[:10]
        return [{"id": t.id, "title": t.name, "artist": t.artist} for t in tracks]

    async def search_songs(self, query: str):
        results = am.search(query=query)[:10]
        return [{"id": t.id, "title": t.name, "artist": t.artist} for t in results]

    async def play_song(self, song_id: str):
        track = am.get_track(song_id)
        os.system(f'cvlc --play-and-exit "{track.getUrl()}"')
        return {"status": "playing", "song_id": song_id}

    async def _main(self):
        pass

    async def _unload(self):
        pass
