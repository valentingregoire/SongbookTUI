from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import DataTable, Button, Static

from backend.dto import SongbookDTO, SongDTO
from tui.screens.song_overview.song_overview_modal import SongOverviewModal
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import Spacer


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
    BINDINGS = [
        ("q", "pop_screen", "Quit"),
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
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.songs = songs
        self.songbook = songbook
        self.current_song_index = current_song_index

    def compose(self) -> ComposeResult:
        with Container():
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
                    # yield ActionButton(
                    #     " Close", action="screen.pop_screen", classes="actions-cell"
                    # )
            yield Spacer()
            yield ActionButton(
                " OK", action="pop_screen", id="btn_ok", classes="btn-link success"
            )

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
        if self.current_song_index == 0:
            return
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index -= 1
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    async def action_down(self):
        if self.current_song_index == len(self.songbook.songs) - 1:
            return
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index += 1
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    def action_add(self) -> None:
        self.app.push_screen(
            SongOverviewModal(
                songs=self.songs,
                songbook=self.songbook,
                current_song_index=self.current_song_index,
            )
        )

    def action_remove(self, index: int):
        self.songbook.songs.pop(index)
        if index == self.current_song_index:
            self.current_song_index = 0
        elif index < self.current_song_index:
            self.current_song_index -= 1
        if len(self.songbook.songs) == 0:
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
