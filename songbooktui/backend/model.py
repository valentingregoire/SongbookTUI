from dataclasses import dataclass
from enum import StrEnum


class FileType(StrEnum):
    TEXT = "txt"
    MARKDOWN = "md"


class SettingsType(StrEnum):
    DEFAULT = "default"
    USER = "user"


@dataclass
class Page:
    """Model class that represents a page."""

    content: str
    file_type: FileType = FileType.TEXT


@dataclass
class Song:
    """Model class that represents a song."""

    id: int
    title: str
    pages: list[Page]
    artist: str | None = None


@dataclass
class Songbook:
    """Model class that represents a songbook.

    The song_ids are the ids of the songs in the songbook. They are stored in the corresponding JSON file.
    The songs are the actual song objects. They are loaded after the song_ids are read from the JSON file.
    """

    id: int
    name: str
    songs: list[int]


@dataclass
class Settings:
    default_songbook: str | None = None
