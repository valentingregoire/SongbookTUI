from backend import dao
from backend.dto import SongbookDTO, SongDTO
from backend.model import Song


async def get_songs() -> dict[int, SongDTO]:
    """Get all songs from the filesystem."""

    songs_data: tuple[Song] = await dao.read_songs()
    songs = {s.id: song_to_dto(s) for s in songs_data}
    return songs


def _get_songbook_names() -> list[str]:
    """Get all songbook names from the filesystem."""

    file_names = dao.get_songbook_files()
    return [file_name.split("/")[-1][:-5] for file_name in file_names]


async def get_songbooks(songs: dict[int, SongDTO]) -> dict[str, SongbookDTO]:
    """Get all songbooks from the filesystem."""

    songbooks_data = await dao.read_songbooks()
    songbooks = {}
    for sd in songbooks_data:
        songs = [song for sid, song in songs.items() if sid in sd.songs]
        songbook = SongbookDTO(name=sd.name, songs=songs)
        songbooks[sd.name] = songbook
    return songbooks


# DTO Conversion Functions
def song_to_dto(song: Song) -> SongDTO:
    """Convert a Song object to a SongDTO object."""

    return SongDTO(
        id=song.id,
        title=song.title,
        pages=song.pages,
        artist=song.artist,
    )