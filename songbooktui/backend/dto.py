from dataclasses import dataclass, field

from backend.model import FileType


@dataclass
class PageDTO:
    content: str
    file_type: FileType


@dataclass
class SongDTO:
    id: int
    title: str
    pages: list[PageDTO] | None = None
    raw_pages: list[PageDTO] | None = None
    artist: str | None = None
    key: str | None = None
    bpm: int | None = None
    duration: int | None = None
    auto_paginate: bool = False

    @property
    def full_title(self) -> str:
        return f"{self.artist} - {self.title}" if self.artist else self.title

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other) -> bool:
        return self.id == other.id if other else False


@dataclass(frozen=True)
class SongbookDTO:
    """Model class that represents a songbook.

    The name should always be unique, it is used as an identifier.
    The song_ids are the ids of the songs in the songbook. They are stored in the corresponding JSON file.
    The songs are the actual song objects. They are loaded after the song_ids are read from the JSON file.
    """

    id: int | None = None
    name: str | None = None
    songs: list[SongDTO] = field(default_factory=lambda: [])

    @property
    def size(self) -> int:
        return len(self.songs)

    def __hash__(self) -> int:
        return self.id
