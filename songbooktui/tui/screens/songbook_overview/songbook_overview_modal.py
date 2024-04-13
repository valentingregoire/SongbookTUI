from backend.dto import SongbookDTO, SongDTO
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import DataTable, Static
from tui.screens.song_overview.song_overview_modal import SongOverviewModal
from tui.utils import DEFAULT_BINDINGS, cancel, ok
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import ActionsBar, CenterFloat


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
    BINDINGS = DEFAULT_BINDINGS + [
        ("a", "add", "Add/Remove"),
    ]

    songs: dict[int, SongDTO]
    songbook: SongbookDTO
    current_song_index: int

    def __init__(
        self,
        songs: dict[int, SongDTO],
        songbook: SongbookDTO,
        current_song_index: int,
        name: str | None = None,
        p_id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, p_id, classes)
        self.songs = songs
        self.songbook = songbook
        self.current_song_index = current_song_index

    def compose(self) -> ComposeResult:
        # yield Static("[b]Songbook Overview", id="title")
        with Vertical(classes="center-middle"):
            with CenterFloat(classes="w-full primary"):
                yield Static(f"[b]{self.songbook.name}")
            with Horizontal(id="container"):
                yield DataTable(id="data-table", classes="right-middle")
                with Vertical(id="container-actions", classes="left-middle"):
                    yield Static("[b]Actions", classes="title-bar")
                    yield ActionButton(
                        " Move Up",
                        action=f"screen.up({self.current_song_index})",
                        classes="btn-action left-middle",
                    )
                    yield ActionButton(
                        " Move Down",
                        action=f"screen.down({self.current_song_index})",
                        classes="btn-action left-middle",
                    )
                    yield ActionButton(
                        " Add",
                        action=f"screen.add({self.current_song_index})",
                        classes="btn-action left-middle",
                    )
                    yield ActionButton(
                        " Delete",
                        action=f"screen.remove({self.current_song_index})",
                        classes="btn-action left-middle",
                    )
                    yield ActionButton(
                        " Close", action="screen.pop_screen", classes="actions-cell"
                    )
            # yield Spacer()
            # with HorizontalFloat():
            #     with RightFloat(classes="width-full"):
            with ActionsBar():
                yield ActionButton(
                    cancel(), action="pop_screen", classes="btn-link error"
                )
                yield ActionButton(ok(), action="screen.ok", classes="btn-link success")

    async def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Title", "Artist")
        table.cursor_type = "row"
        await self.populate_table(table)

    async def populate_table(self, table: DataTable = None) -> None:
        if not table:
            table = self.query_one(DataTable)
        table.clear()
        for index, song in enumerate(self.songbook.songs):
            table.add_row(
                song.title,
                song.artist or "",
                # f"[@click=up({index})]  [/] [@click=down({index})]  [/] [@click=add({index})]  [/] [@click=remove({index})]  [/]",
                label=f"{index + 1}",
                key=str(index),
            )
        table.cursor_coordinate = Coordinate(row=self.current_song_index, column=0)

    def action_ok(self) -> None:
        self.dismiss((self.songbook, self.current_song_index))

    def action_clear_table(self) -> None:
        table = self.query_one(DataTable)
        table.rows.clear()

    def on_data_table_row_selected(self, selected_row: DataTable.RowSelected) -> None:
        self.current_song_index = selected_row.cursor_row

    async def action_up(self):
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index = (self.current_song_index + self.songbook.size) % (
            self.songbook.size + 1
        )
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    async def action_down(self):
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index = (self.current_song_index + 1) % (self.songbook.size + 1)
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    def action_add(self) -> None:
        def fallback(data: list[SongDTO]) -> None:
            self.songbook.songs = data
            # self.recompose()
            # self.app.recompose()

        self.app.push_screen(
            SongOverviewModal(
                songs=self.songs,
                songbook=self.songbook,
                current_song_index=self.current_song_index,
            ),
            fallback,
        )

    def action_remove(self, index: int):
        self.songbook.songs.pop(index)
        if index == self.current_song_index:
            self.current_song_index = 0
        elif index < self.current_song_index:
            self.current_song_index -= 1
        if self.songbook.size == 0:
            self.app.pop_screen()
        else:
            # self.recompose()
            # self.app.recompose()
            self.app.pop_screen()
            self.app.push_screen(
                SongbookOverviewModal(
                    songs=self.songs,
                    songbook=self.songbook,
                    current_song_index=self.current_song_index,
                )
            )
