from dataclasses import dataclass


@dataclass
class BaseDTO:
    name: str


@dataclass
class SongDTO:
    id: int
    title: str
    pages: list[str]
    artist: str | None = None


@dataclass
class SongbookDTO(BaseDTO):
    """Model class that represents a songbook.

    The name should always be unique, it is used as an identifier.
    The song_ids are the ids of the songs in the songbook. They are stored in the corresponding JSON file.
    The songs are the actual song objects. They are loaded after the song_ids are read from the JSON file.
    """

    songs: list[SongDTO]
