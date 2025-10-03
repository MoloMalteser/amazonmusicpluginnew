import { definePlugin, ServerAPI } from "decky-frontend-lib";
import { useState, useEffect } from "react";

export default definePlugin((serverAPI?: ServerAPI) => {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [recent, setRecent] = useState<any[]>([]);
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const fetchRecommendations = async () => {
    const recs = await serverAPI!.callPluginMethod("recommendations", {});
    setRecommendations(recs);
  };

  const fetchRecentlyPlayed = async () => {
    const recentSongs = await serverAPI!.callPluginMethod("recently_played", {});
    setRecent(recentSongs);
  };

  const searchSongs = async () => {
    if (!query) return;
    const results = await serverAPI!.callPluginMethod("search_songs", { query });
    setSearchResults(results);
  };

  const playSong = async (song_id: string) => {
    await serverAPI!.callPluginMethod("play_song", { song_id });
    fetchRecentlyPlayed();
  };

  useEffect(() => {
    fetchRecommendations();
    fetchRecentlyPlayed();
  }, []);

  return (
    <div style={{ padding: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <input
          type="text"
          placeholder="Suche..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={searchSongs}>Suchen</button>
        <button>Profil</button>
      </div>

      <h3>Song-Empfehlungen (Amazon)</h3>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        {recommendations.map((song) => (
          <div
            key={song.id}
            style={{ border: "1px solid gray", padding: 5, cursor: "pointer" }}
            onClick={() => playSong(song.id)}
          >
            {song.title} <br /> <small>{song.artist}</small>
          </div>
        ))}
      </div>

      <h3>Zuletzt gehört</h3>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        {recent.map((song) => (
          <div
            key={song.id}
            style={{ border: "1px solid gray", padding: 5, cursor: "pointer" }}
            onClick={() => playSong(song.id)}
          >
            {song.title} <br /> <small>{song.artist}</small>
          </div>
        ))}
      </div>

      <h3>Suchergebnisse</h3>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        {searchResults.map((song) => (
          <div
            key={song.id}
            style={{ border: "1px solid gray", padding: 5, cursor: "pointer" }}
            onClick={() => playSong(song.id)}
          >
            {song.title} <br /> <small>{song.artist}</small>
          </div>
        ))}
      </div>
    </div>
  );
});
