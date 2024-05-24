from art import text2art
import importlib.metadata


SONGBOOK = "󰁧 "
SONG = "󰎈 "
CHECKMARK = " "
# _CROSSMARK = " "
CROSSMARK = " "
PENSIL = " "
OPEN_FOLDER = " "
FLOPPY = "󰉉 "

TITLE = text2art("Songbooks", font="doom")

VERSION = importlib.metadata.version("SongbookTUI")

DEFAULT_BINDINGS = [
    ("o", "ok", "Ok"),
    ("c", "pop_screen", "Cancel"),
    ("q", "exit", "Quit"),
]


def ok(text: str = "OK") -> str:
    return f"{CHECKMARK}{text}"


def cancel(text: str = "Cancel") -> str:
    return f"{CROSSMARK}{text}"
