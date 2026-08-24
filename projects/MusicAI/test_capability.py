import importlib

import pytest


@pytest.fixture
def app_module(monkeypatch, tmp_path):
    monkeypatch.setenv("FLASK_SECRET_KEY", "test-session-secret")
    monkeypatch.setenv("MUSICAI_TOKEN_SECRET", "test-token-secret")
    monkeypatch.setenv("MUSICAI_SQLITE_PATH", str(tmp_path / "musicai.db"))
    import musicAI
    import musicai_secure_store

    importlib.reload(musicai_secure_store)
    return importlib.reload(musicAI)


def test_oauth_callback_requires_matching_state(app_module):
    app = app_module.application
    app.config.update(TESTING=True)

    with app.test_request_context("/callback?state=received"):
        assert app_module._valid_oauth_state("youtube_music") is False

    with app.test_request_context("/callback"):
        app_module.flask.session["oauth_state_youtube_music"] = "expected"
        assert app_module._valid_oauth_state("youtube_music") is False

    with app.test_request_context("/callback?state=received"):
        app_module.flask.session["oauth_state_youtube_music"] = "expected"
        assert app_module._valid_oauth_state("youtube_music") is False

    with app.test_request_context("/callback?state=expected"):
        app_module.flask.session["oauth_state_youtube_music"] = "expected"
        assert app_module._valid_oauth_state("youtube_music") is True


def test_roadmap_provider_routes_are_honestly_unavailable(app_module):
    client = app_module.application.test_client()

    spotify = client.get("/providers/spotify/connect")
    soundcloud = client.get("/providers/soundcloud/connect")

    assert spotify.status_code == 503
    assert b"roadmap" in spotify.data.lower()
    assert soundcloud.status_code == 503
    assert b"roadmap" in soundcloud.data.lower()


def test_account_provider_token_and_analysis_survive_new_connections(app_module):
    store = app_module.token_store
    account_id = store.resolve_account("youtube_music", "google-1", {"name": "Listener"})
    linked_id = store.resolve_account("spotify", "spotify-1", {"display_name": "Listener"}, preferred_user_id=account_id)
    store.save_provider_token(account_id, "youtube_music", {"access_token": "secret-token"}, provider_account_id="google-1")

    assert linked_id == account_id
    assert set(store.connected_providers(account_id)) == {"youtube_music", "spotify"}
    assert store.load_provider_token(account_id, "youtube_music") == {"access_token": "secret-token"}

    saved = store.save_cached_analysis(account_id, "youtube_music", "song", "song-1", "v1", "lyrics", {"subjects": ["hope"]})
    loaded = store.load_cached_analysis(account_id, "youtube_music", "song", "song-1", "v1", "lyrics")
    assert saved["cache"]["hit"] is False
    assert loaded["cache"]["hit"] is True
    assert loaded["subjects"] == ["hope"]


def test_lyrics_fallback_precedes_metadata_analysis(app_module, monkeypatch):
    monkeypatch.setattr(app_module, "_find_genius_song", lambda title, artist="": {"title": title, "artist": artist, "url": "https://genius.test/song"})
    monkeypatch.setattr(app_module, "_scrape_genius_lyrics", lambda url: None)
    monkeypatch.setattr(app_module, "_fetch_lyrics_ovh", lambda title, artist="": "Hope rises in the city\nLove carries us home")
    monkeypatch.setattr(app_module.watson, "ai_to_Text", lambda text: (_ for _ in ()).throw(RuntimeError("offline")))

    analysis, warning, _ = app_module.analyze_song_lyrics_safely("Home", "Artist", fallback_text="metadata only")

    assert analysis["lyrics_found"] is True
    assert analysis["analyzed_text_source"] == "lyrics"
    assert analysis["lyrics_line_count"] == 2
    assert warning == "offline"


def test_aggregate_keeps_traceable_song_entities_subjects_keywords_and_concepts(app_module):
    aggregate = app_module._aggregate_track_analyses([
        {
            "title": "Song A",
            "channel": "Artist A",
            "analysis": {
                "overall_emotion": {"joy": 0.8},
                "sentiment": {"label": "positive"},
                "keywords": [{"text": "freedom"}],
                "entities": [{"text": "Harlem"}],
                "subjects": ["community"],
                "concepts": ["music"],
                "relations": ["artist creates song"],
                "lyrics_found": True,
            },
        }
    ])

    assert aggregate["top_keywords"] == [("freedom", 1)]
    assert aggregate["top_entities"] == [("Harlem", 1)]
    assert aggregate["top_subjects"] == [("community", 1)]
    assert aggregate["top_concepts"] == [("music", 1)]
    assert aggregate["tracks"][0]["title"] == "Song A"
    assert aggregate["tracks"][0]["entities"] == [{"text": "Harlem"}]
