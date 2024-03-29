from dataclasses import dataclass


@dataclass
class Song:
    """Model class that represents a song."""

    id: int
    title: str
    pages: list[str]
    artist: str | None = None


@dataclass
class Songbook:
    """Model class that represents a songbook.

    The song_ids are the ids of the songs in the songbook. They are stored in the corresponding JSON file.
    The songs are the actual song objects. They are loaded after the song_ids are read from the JSON file.
    """

    name: str
    songs: list[int]
