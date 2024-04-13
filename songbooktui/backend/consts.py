import os

from backend.model import FileType

_HOME = os.path.expanduser("~")
BASE_LOCATION = f"{_HOME}/.songbooks"
SONGS_NAMESPACE = "songs"
SONGBOOKS_NAMESPACE = "songbooks"
SONGS_LOCATION = f"{BASE_LOCATION}/{SONGS_NAMESPACE}"
SONGBOOKS_LOCATION = f"{BASE_LOCATION}/{SONGBOOKS_NAMESPACE}"
INFO = ".info.json"

DEFAULT_FILE_TYPE = FileType.TEXT
