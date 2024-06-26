import asyncio
import json
import os
from dataclasses import asdict

from backend.consts import SONGBOOKS_LOCATION, SONGS_LOCATION, INFO, SETTINGS_LOCATION
from backend.dto import FileType
from backend.model import Songbook, Song, Page, Settings


async def read_songs() -> tuple[Song]:
    """Read all songs from the filesystem."""
    tasks = []
    song_folders = os.listdir(SONGS_LOCATION)
    for song_folder in song_folders:
        task = asyncio.create_task(read_song(song_folder))
        tasks.append(task)

    song_objects = await asyncio.gather(*tasks)
    return song_objects


async def read_song(folder: str) -> Song:
    """Read a song from the filesystem."""
    folder_path = f"{SONGS_LOCATION}/{folder}"

    # get the id
    song_id = int(folder.split("/")[-1])

    # get the info from the info file
    with open(f"{folder_path}/{INFO}", "r") as json_file:
        song_data = json.loads(json_file.read())

    # get the pages
    pages = []
    files = os.listdir(folder_path)
    page_files = sorted(
        [f for f in files if not f.startswith(".")], key=lambda n: int(n.split(".")[0])
    )
    for page in page_files:
        page_path = f"{folder_path}/{page}"
        if os.path.isfile(page_path):
            file_type = FileType(page.split(".")[-1])
            with open(page_path, "r") as page_file:
                page = Page(content=page_file.read(), file_type=file_type)
                pages.append(page)
            # pages.append(page_path)
    # all gathered data into a Song object
    return Song(id=song_id, pages=pages, raw_pages=pages, **song_data)


async def write_page(page: Page, song_id: int, page_number: int) -> None:
    """Write a page to the filesystem."""
    song_folder = f"{SONGS_LOCATION}/{song_id}"
    with open(f"{song_folder}/{page_number}.{page.file_type}", "w") as page_file:
        page_file.write(page.content)


def get_songbook_files() -> list[str]:
    """Get all songbook files from the filesystem."""

    songbook_files = []
    for filename in os.listdir(SONGBOOKS_LOCATION):
        if filename.endswith(".json"):
            songbook_files.append(f"{SONGBOOKS_LOCATION}/{filename}")
    return songbook_files


async def read_songbooks() -> tuple[Songbook]:
    """Read all songbooks from the filesystem."""

    tasks = []
    for filename in os.listdir(SONGBOOKS_LOCATION):
        if filename.endswith(".json"):
            task = asyncio.create_task(
                read_songbook(f"{SONGBOOKS_LOCATION}/{filename}")
            )
            tasks.append(task)
    songbooks = await asyncio.gather(*tasks)
    return songbooks


async def read_songbook(file: str) -> Songbook:
    """Read a songbook from the filesystem."""
    with open(file, "r") as json_file:
        songbook_data = json.loads(json_file.read())
        songbook: Songbook = Songbook(
            id=songbook_data["id"],
            name=songbook_data["name"],
            songs=songbook_data["songs"],
        )
        return songbook


async def write_songbook(songbook: Songbook) -> None:
    """Write a songbook to the filesystem."""
    with open(f"{SONGBOOKS_LOCATION}/{songbook.id}.json", "w") as json_file:
        data = asdict(songbook)
        json_file.write(json.dumps(data, indent=4))


async def write_song(song: Song) -> None:
    """Write a song to the filesystem."""
    song_folder = f"{SONGS_LOCATION}/{song.id}"
    os.makedirs(song_folder, exist_ok=True)
    info = asdict(song)
    del info["id"]
    del info["pages"]
    del info["raw_pages"]
    with open(f"{song_folder}/{INFO}", "w") as json_file:
        json_file.write(json.dumps(info, indent=4))


async def read_settings() -> Settings:
    """Read the settings from the filesystem."""
    with open(SETTINGS_LOCATION, "r") as settings_file:
        settings_dict = json.loads(settings_file.read())
    settings = Settings(**settings_dict)
    return settings


async def write_settings(settings: dict[str:str]) -> None:
    """Write the settings to the filesystem.

    Args:
        settings (dict[str: str]): the settings to write

    Returns: None
    """
    with open(SETTINGS_LOCATION, "w") as settings_file:
        settings_file.write(json.dumps(settings, indent=4))


# songs = asyncio.run(read_songs())
# print(songs)
# asyncio.run(read_songbooks())
