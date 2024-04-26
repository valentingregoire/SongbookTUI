from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DataTable, Input

from backend.dto import SongDTO


class SongsScreen(Screen):
    CSS_PATH = "songs_screen.tcss"
    songs: dict[int, SongDTO]
    current_song_id: reactive[int] = reactive(0)
    current_song: reactive[SongDTO] = reactive(None)

    def __init__(self, songs: dict[int, SongDTO]) -> None:
        super().__init__()
        self.songs = songs
        # self.current_song_id = list(self.songs.keys())[0]

    def compute_current_song(self) -> SongDTO | None:
        return self.songs.get(self.current_song_id)

    def compose(self) -> ComposeResult:
        table = DataTable(id="songs-table", classes="w-auto")
        table.add_columns("#", "  Title", "󰙃  Artist", "󰽰 ", "󰟚 ", " ")
        table.cursor_type = "row"
        table.border_title = "Songs"
        yield table

        details_container = Vertical(id="song-details-container", classes="h-1fr")
        details_container.border_title = "Details"
        with details_container:
            txt_id = Input(id="txt_id", name="id", placeholder="ID", disabled=True)
            txt_id.border_title = "ID"
            yield txt_id
            txt_title = Input(id="txt_title", name="title", placeholder="Title")
            txt_title.border_title = "  Title"
            yield txt_title
            txt_artist = Input(id="txt_artist", name="artist", placeholder="Artist")
            txt_artist.border_title = "󰙃  Artist"
            yield txt_artist
            txt_key = Input(id="txt_key", name="key", placeholder="Key")
            txt_key.border_title = "󰽰 Key"
            yield txt_key
            txt_bpm = Input(id="txt_bpm", name="bpm", placeholder="BPM")
            txt_bpm.border_title = "󰟚 BPM"
            yield txt_bpm
            txt_duration = Input(
                id="txt_duration", name="duration", placeholder="Duration"
            )
            txt_duration.border_title = "  Duration"
            yield txt_duration

    async def on_mount(self) -> None:
        await self.populate_songs_table()

    async def populate_songs_table(self) -> None:
        table = self.query_one(DataTable)
        for song in self.songs.values():
            table.add_row(
                str(song.id),
                song.title,
                song.artist or "",
                song.key or "",
                str(song.bpm or ""),
                str(song.duration or ""),
            )
