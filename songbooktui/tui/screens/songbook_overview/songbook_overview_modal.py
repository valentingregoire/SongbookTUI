import dataclasses

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import DataTable, Static, Input

from backend import service
from backend.dto import SongbookDTO, SongDTO
from tui.screens.song_overview.song_overview_modal import SongOverviewModal
from tui.utils import DEFAULT_BINDINGS
from tui.widgets.action_button import ActionButton
from tui.widgets.toggle import Toggle
from tui.widgets.widget_factory import WidgetFactory


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
    BINDINGS = DEFAULT_BINDINGS + [("a", "add", "Add/Remove"), ("e", "edit", "Edit")]

    songs: dict[int, SongDTO]
    songbook: SongbookDTO
    current_song_index: int
    read_only_mode: reactive[bool] = reactive(True)
    edit_mode: reactive[bool] = reactive(True)
    zebra_stripes: reactive[bool] = reactive(True)

    def __init__(
        self,
        songs: dict[int, SongDTO],
        songbook: SongbookDTO,
        current_song_index: int = 0,
        read_only_mode: bool = True,
        name: str | None = None,
        p_id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, p_id, classes)
        self.songs = songs
        self.songbook = dataclasses.replace(songbook, songs=songbook.songs.copy())
        self.current_song_index = current_song_index
        self.read_only_mode = read_only_mode

    def compose(self) -> ComposeResult:
        with Vertical(classes="center-middle"):
            # with CenterFloat(classes="w-full primary"):
            #     yield Static(f"[b]{self.songbook.name}")
            new_name_input = Input(placeholder="Name", value=self.songbook.name)
            new_name_input.border_title = "Name"
            yield new_name_input.data_bind(
                disabled=SongbookOverviewModal.read_only_mode
            )
            with Horizontal(id="container"):
                table = DataTable(id="data-table", classes="right-middle")
                table.add_columns("Title", "Artist")
                table.cursor_type = "row"
                yield table
                with Vertical(
                    id="container-actions",
                    classes="left-middle disabled",
                ).data_bind(disabled=SongbookOverviewModal.read_only_mode):
                    yield Static("[b]Actions", classes="title-bar")
                    yield ActionButton(" Up", action="screen.up")
                    yield ActionButton(" Down", action="screen.down")
                    yield ActionButton(" Add", action="screen.add")
                    yield ActionButton(" Delete", action="screen.remove")

            toggle_container = Horizontal(classes="w-auto")
            toggle_label = Static("[b] Edit")
            toggle = Toggle("screen.edit").data_bind(value=self.edit_mode)
            toggle_container.compose_add_child(toggle_label)
            toggle_container.compose_add_child(toggle)
            yield WidgetFactory.actions_bar(
                [
                    toggle_container,
                    WidgetFactory.btn_cancel(),
                    WidgetFactory.btn_save(),
                ]
            )

    async def on_mount(self) -> None:
        await self.populate_table()

    async def populate_table(self, table: DataTable = None) -> None:
        if not table:
            table = self.query_one(DataTable)
        table.clear()
        # table.rows.clear()
        for index, song in enumerate(self.songbook.songs):
            table.add_row(
                song.title,
                song.artist or "",
                label=f"{index + 1}",
                key=str(index),
            )
        table.cursor_coordinate = Coordinate(row=self.current_song_index, column=0)

    def compute_edit_mode(self) -> bool:
        return not self.read_only_mode

    def action_edit(self) -> None:
        self.read_only_mode = not self.read_only_mode
        container_actions = self.query_one("#container-actions", Vertical)
        if self.read_only_mode:
            container_actions.add_class("disabled")
        else:
            container_actions.remove_class("disabled")

    async def action_save(self, save: bool = True) -> None:
        if save:
            self.songbook = dataclasses.replace(
                self.songbook, name=self.query_one(Input).value
            )
            await service.save_songbook(self.songbook)
            self.dismiss((self.current_song_index, self.songbook))
        else:
            self.dismiss(self.current_song_index)

    def on_data_table_row_selected(self, selected_row: DataTable.RowSelected) -> None:
        self.current_song_index = selected_row.cursor_row
        if self.read_only_mode:
            self.action_save(False)

    async def action_up(self):
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index = (self.current_song_index + self.songbook.size) % (
            self.songbook.size + 1
        )
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    async def action_down(self):
        song = self.songbook.songs.pop(self.current_song_index)
        self.current_song_index = (self.current_song_index + 1) % (
            self.songbook.size + 1
        )
        self.songbook.songs.insert(self.current_song_index, song)
        await self.populate_table()

    async def action_add(self) -> None:
        async def fallback(data: list[SongDTO]) -> None:
            self.songbook = dataclasses.replace(self.songbook, songs=data)
            # self.songbook.songs = data
            await self.populate_table()

        await self.app.push_screen(
            SongOverviewModal(
                songs=self.songs,
                songbook=self.songbook,
                current_song_index=self.current_song_index,
            ),
            fallback,
        )

    async def action_remove(self):
        self.songbook.songs.pop(self.current_song_index)
        if self.current_song_index > 0:
            self.current_song_index -= 1
        await self.populate_table()
