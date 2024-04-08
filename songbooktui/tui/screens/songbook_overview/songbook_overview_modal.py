from textual.app import ComposeResult
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.coordinate import Coordinate
from textual.screen import Screen, ModalScreen
from textual.widgets import Static, DataTable, Button

from backend.dto import SongbookDTO, SongDTO
from tui.screens.song_overview.song_overview_modal import SongOverviewModal
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import RightFloat, LeftFloat, TopBar, HorizontalFloat, Spacer


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
    BINDINGS = [
        ("q", "pop_screen", "Quit"),
        ("a", f"add({0}", "Add/Remove"),
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
        # with TopBar():
        #     with LeftFloat():
        #         pass
        #     with CenterFloat():
        #         yield Static(f"󱍙  {self.songbook.name}")
        #     with Vertical(id="songbook-overview-modal-container"):
            # with RightFloat():

            # with Vertical(id="title-bar"):
            #     with CenterFloat():

        # with HorizontalFloat():
        #     with LeftFloat():
        #         yield Static(f"󱍙  {self.songbook.name}")
        #     with RightFloat():
        #             # with RightFloat():
        #         yield ActionButton("", id="btn_close", action="pop_screen")
        # with RightFloat():
        with Horizontal(id="container"):
            yield DataTable(id="data-table", classes="right-middle")
            with Vertical(id="container-actions", classes="left-middle"):
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
        # with RightFloat():
            # yield Static("[@click=pop_screen] OK[/]", id="btn_ok", classes="btn-link success")
        with Horizontal(classes="actions-row"):
            yield ActionButton(" OK", action="pop_screen", id="btn_ok", classes="btn-link success")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        # table.add_columns("Title", "Artist", "Actions")
        table.add_columns("Title", "Artist")
        table.cursor_type = "row"
        for index, song in enumerate(self.songbook.songs):
            table.add_row(
                song.title,
                song.artist or "",
                # f"[@click=up({index})]  [/] [@click=down({index})]  [/] [@click=add({index})]  [/] [@click=remove({index})]  [/]",
                label=f"{index + 1}",
                key=str(index)
            )
        table.cursor_coordinate = Coordinate(row=self.current_song_index, column=0)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_ok":
            self.app.pop_screen()

    # def compose_ori(self) -> ComposeResult:
    #     with Grid(id="table"):
    #         with TopBar(id="title-bar"):
    #             with LeftFloat():
    #                 pass
    #             with CenterFloat():
    #                 yield Static(f"󱍙  {self.songbook.name}")
    #             with RightFloat():
    #                 yield ActionButton("", id="btn_close", action="pop_screen")
    #         with TopBar(id="actions-bar"):
    #             # with LeftFloat():
    #             #     pass
    #             # with CenterFloat():
    #             #     pass
    #             with RightFloat(id="actions-bar-right"):
    #                 yield ActionButton(
    #                     "  Show", action="screen.go", classes="actions-cell"
    #                 )
    #                 yield ActionButton(
    #                     " Move Up",
    #                     action=f"screen.up({self.current_song_index})",
    #                     classes="actions-cell",
    #                 )
    #                 yield ActionButton(
    #                     " Move Down",
    #                     action=f"screen.down({self.current_song_index})",
    #                     classes="actions-cell",
    #                 )
    #                 yield ActionButton(
    #                     " Add",
    #                     action=f"screen.add({self.current_song_index})",
    #                     classes="actions-cell",
    #                 )
    #                 yield ActionButton(
    #                     " Delete",
    #                     action=f"screen.remove({self.current_song_index})",
    #                     classes="actions-cell",
    #                 )
    #         yield Static("", classes="spacer")
    #         yield Static("#", classes="header-cell")
    #         yield Static("Title", classes="header-cell")
    #         yield Static("Artist", classes="header-cell")
    #         yield Static("Actions", classes="header-cell")
    #         for index, song in enumerate(self.songbook.songs):
    #             yield Static(str(index + 1), classes="cell")
    #             yield Static(
    #                 f"[@click=screen.set_current_song_index({index})]{song.title}[/]",
    #                 classes="cell",
    #             )
    #             yield Static(song.artist or "", classes="cell")
    #             with Horizontal(classes="actions-container"):
    #                 # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
    #                 # yield Static(f"[@click=down({index})]  [/]", classes="actions-cell")
    #                 # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
    #                 yield ActionButton(
    #                     "", action=f"screen.up({index})", classes="actions-cell"
    #                 )
    #                 yield ActionButton(
    #                     "", action=f"screen.down({index})", classes="actions-cell"
    #                 )
    #                 # yield ActionButton(
    #                 #     " ", action=f"screen.add({index})", classes="actions-cell"
    #                 # )
    #                 yield ActionButton(
    #                     "", action=f"screen.remove({index})", classes="actions-cell"
    #                 )

    def on_data_table_row_selected(self, selected_row: DataTable.RowSelected) -> None:
        self.current_song_index = selected_row.cursor_row

    # goes with compose_ori
    # def action_set_current_song_index(self, index: int) -> None:
    #     self.current_song_index = index

    def action_up(self, index: int):
        print("action_up")
        if index == 0:
            return
        song = self.songbook.songs.pop(index)
        self.songbook.songs.insert(index - 1, song)
        # self.recompose()
        # recompose doesn't work, hacky close and reopen
        self.app.pop_screen()
        self.app.push_screen(
            SongbookOverviewModal(
                songs=self.songs,
                songbook=self.songbook,
                current_song_index=self.current_song_index,
            )
        )
        print([s.title for s in self.songbook.songs])

    def action_down(self, index: int):
        print("action_down")
        if index == len(self.songbook.songs) - 1:
            return
        song = self.songbook.songs.pop(index)
        self.songbook.songs.insert(index + 1, song)
        # self.recompose()
        self.app.pop_screen()
        self.app.push_screen(
            SongbookOverviewModal(
                songs=self.songs,
                songbook=self.songbook,
                current_song_index=self.current_song_index,
            )
        )
        print([s.title for s in self.songbook.songs])

    def action_add(self, index: int):
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
        print([s.title for s in self.songbook.songs])
