import asyncio
import json
import os

from backend.consts import SONGBOOKS_LOCATION, SONGS_LOCATION, INFO
from backend.model import Songbook, Song


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
    page_files = sorted([f for f in files if not f.startswith(".")], key=lambda n: int(n.split(".")[0]))
    for page in page_files:
        page_path = f"{folder_path}/{page}"
        if os.path.isfile(page_path):
            pages.append(page_path)
    # all gathered data into a Song object
    song: Song = Song(id=song_id, pages=pages, **song_data)
    return song


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
        songbook_data["name"] = file.split("/")[-1][:-5]
        songbook: Songbook = Songbook(**songbook_data)
        return songbook


# songs = asyncio.run(read_songs())
# print(songs)
# asyncio.run(read_songbooks())
