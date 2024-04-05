from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DataTable

from backend.model import Songbook


class SongbookOverviewTable(VerticalScroll):
    DEFAULT_CSS = """
    SonbookOverviewTable {
        width: 50%;
        height: 50%;
    }
    
    DataTable {
        width: 50%;
        height: 50%;
    }
    """
    songbook: Songbook
    current_song_index: int

    def __init__(self, songbook: Songbook, current_song_index: int = 0, id: str | None = None) -> None:
        super().__init__(id=id)
        self.songbook = songbook
        self.current_song_index = current_song_index

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        current_song = self.songbook.songs[self.current_song_index]
        table = self.query_one(DataTable)
        table.focus()
        table.add_columns("#", "Title", "Artist", "Actions")
        table.cursor_type = "row"
        for index, song in enumerate(self.songbook.songs):
            table.add_row(str(index + 1), current_song.title, current_song.artist, "A", key=index)
