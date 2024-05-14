from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DataTable, Input

from backend.dto import SongDTO
from tui.widgets.action_button import ActionButton
from tui.widgets.widget_factory import WidgetFactory


class SongsScreen(Screen):
    CSS_PATH = "songs_screen.tcss"
    songs: dict[int, SongDTO]
    current_song_id: reactive[int] = reactive(0)
    current_song: reactive[SongDTO] = reactive(None)

    def __init__(self, songs: dict[int, SongDTO]) -> None:
        super().__init__()
        self.songs = songs
        self.current_song_id = list(self.songs.keys())[0]
        # self.current_song_id = list(self.songs.keys())[0]

    def compute_current_song(self) -> SongDTO | None:
        return self.songs.get(self.current_song_id)

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            table = DataTable(id="songs-table", classes="w-auto")
            table.add_columns("  Title", "󰙃  Artist", "󰽰 ", "󰟚 ", " ")
            table.cursor_type = "row"
            table.border_title = "Songs"
            yield table
            details_container = Vertical(id="song-details-container", classes="h-1fr")
            details_container.border_title = "Details"
            with details_container:
                txt_id = Input(id="txt_id", name="id", placeholder="ID", disabled=True)
                txt_id.border_title = "ID"
                yield txt_id
                txt_title = Input(
                    # self.current_song.title,
                    id="txt_title",
                    name="title",
                    placeholder="Title",
                )
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
            yield WidgetFactory.actions_bar(
                [
                    ActionButton(
                        " Previous", action="screen.previous", classes="btn-link"
                    ),
                    WidgetFactory.btn_save(),
                    ActionButton("Next ", action="screen.next", classes="btn-link"),
                ]
            )

    async def on_mount(self) -> None:
        await self.populate_form()
        await self.populate_songs_table()

    async def action_previous(self) -> None:
        table = self.query_one(DataTable)
        row_index = (
            table.cursor_row - 1 if table.cursor_row > 0 else len(table.rows) - 1
        )
        self.current_song_id = int(
            table.coordinate_to_cell_key(Coordinate(row_index, 0)).row_key.value
        )
        await self.populate_form()
        await self.populate_songs_table(row_index)

    async def action_next(self) -> None:
        table = self.query_one(DataTable)
        row_index = (
            table.cursor_row + 1 if table.cursor_row < len(table.rows) - 1 else 0
        )
        self.current_song_id = int(
            table.coordinate_to_cell_key(Coordinate(row_index, 0)).row_key.value
        )
        await self.populate_form()
        await self.populate_songs_table(row_index)

    async def populate_form(self) -> None:
        self.query_one("#txt_id", Input).value = str(self.current_song.id)
        self.query_one("#txt_title", Input).value = self.current_song.title
        self.query_one("#txt_artist", Input).value = self.current_song.artist or ""
        self.query_one("#txt_key", Input).value = self.current_song.key or ""
        self.query_one("#txt_bpm", Input).value = str(self.current_song.bpm or "")
        self.query_one("#txt_duration", Input).value = str(
            self.current_song.duration or ""
        )

    async def populate_songs_table(self, index: int = 0) -> None:
        table = self.query_one(DataTable)
        table.clear()
        for song in self.songs.values():
            table.add_row(
                # str(song.id),
                song.title,
                song.artist or "",
                song.key or "",
                str(song.bpm or ""),
                str(song.duration or ""),
                label=str(song.id),
                key=str(song.id),
            )
        # for some reason, the cursor doesn't move on its own after a click
        table.cursor_coordinate = Coordinate(row=index, column=0)

    async def on_data_table_row_selected(
        self, selected_row: DataTable.RowSelected
    ) -> None:
        self.current_song_id = int(selected_row.row_key.value)
        await self.populate_form()
        await self.populate_songs_table(selected_row.cursor_row)
