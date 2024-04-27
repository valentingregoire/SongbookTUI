import dataclasses

from rich import box
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DataTable, Input, Static

from backend.dto import SongDTO, SongbookDTO
from backend.model import Settings
from tui.screens.songbook_overview.songbook_overview_modal import SongbookOverviewModal
from tui.utils import ok
from tui.widgets.widget_factory import WidgetFactory


class SongbooksScreen(Screen):
    CSS_PATH = "songbooks_screen.tcss"

    songbooks: dict[int, SongbookDTO]
    songs: dict[int, SongDTO]
    settings: Settings

    current_songbook_id: reactive[int] = reactive(0)
    current_songbook: reactive[SongbookDTO] = reactive(None)
    current_songbook_name: reactive[str] = reactive("")

    def __init__(
        self,
        songbooks: dict[int, SongbookDTO],
        songs: dict[int, SongDTO],
        settings: Settings,
    ) -> None:
        super().__init__()
        self.songbooks = songbooks
        self.songs = songs
        self.settings = settings
        self.current_songbook_id = self.settings.default_songbook

    def compute_current_songbook(self) -> SongbookDTO:
        return self.songbooks[self.current_songbook_id]

    def compute_current_songbook_name(self) -> str:
        return self.current_songbook.name

    def compose(self) -> ComposeResult:
        table = DataTable(id="songbooks-table", classes="w-auto")
        table.add_columns("Name", "Songs")
        table.cursor_type = "row"
        table.border_title = "Songbooks"
        yield table
        details_container = Vertical(id="songbook-details-container", classes="h-1fr")
        details_container.border_title = "Details"
        with details_container:
            txt_name = Input(
                id="txt_name",
                name="name",
                placeholder="Name",
                disabled=True,
            ).data_bind(value=SongbooksScreen.current_songbook_name)
            txt_name.border_title = "Name"
            yield txt_name
            yield Static(id="stc_songs", markup=True)
        yield WidgetFactory.actions_bar(
            [WidgetFactory.btn_edit(), WidgetFactory.btn_ok()]
        )

    async def on_mount(self) -> None:
        await self.populate_songbook_table()

    async def action_edit(self) -> None:
        async def fallback(data: tuple[int, SongbookDTO] | int) -> None:
            if isinstance(data, tuple):
                # we don't need the current song index which is in index 0
                songbook = data[1]
                self.songbooks[songbook.id] = dataclasses.replace(songbook)
                self.notify(ok(f" Songbook {self.current_songbook_name} saved."))
                # await self.populate_song_list()
                await self.populate_songs_table()

        await self.app.push_screen(
            SongbookOverviewModal(
                songs=self.songs, songbook=self.current_songbook, read_only_mode=False
            ),
            fallback,
        )

    async def populate_songbook_table(self) -> None:
        table = self.query_one("#songbooks-table", DataTable)
        table.clear()
        default_row = 0
        for index, songbook in enumerate(self.songbooks.values()):
            table.add_row(
                # str(songbook.id),
                songbook.name,
                str(songbook.size),
                label=str(songbook.id),
                key=str(songbook.id),
            )
            if songbook.id == self.settings.default_songbook:
                default_row = index

        table.cursor_coordinate = Coordinate(row=default_row, column=0)
        await self.populate_songs_table()

    async def populate_songs_table(self) -> None:
        stc_songs = self.query_one(Static)
        table = Table(title="🎶 Songs", box=box.ROUNDED)
        table.add_column("  Title")
        table.add_column("󰙃  Artist")
        table.add_column("󰽰 ")
        table.add_column("󰟚 ")
        table.add_column(" ")

        for song in self.current_songbook.songs:
            table.add_row(
                song.title,
                song.artist,
                song.key,
                song.bpm,
                song.duration,
            )

        stc_songs.update(table)

    async def on_data_table_row_selected(
        self, selected_row: DataTable.RowSelected
    ) -> None:
        self.current_songbook_id = int(selected_row.row_key.value)
        await self.populate_songs_table()
