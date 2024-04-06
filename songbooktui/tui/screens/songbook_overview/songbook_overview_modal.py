from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Static

from backend.dto import SongbookDTO, SongDTO
from tui.screens.song_overview.song_overview_modal import SongOverviewModal
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import TopBar, LeftFloat, RightFloat, CenterFloat


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
        with Grid(id="table"):
            with TopBar(id="title-bar"):
                with LeftFloat():
                    pass
                with CenterFloat():
                    yield Static(self.songbook.name)
                with RightFloat():
                    yield ActionButton("", id="btn_close", action="pop_screen")
            with TopBar(id="actions-bar"):
                with LeftFloat():
                    pass
                with CenterFloat():
                    pass
                with RightFloat():
                    yield ActionButton(
                        " Move Up", action=f"screen.up({self.current_song_index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        " Move Down", action=f"screen.down({self.current_song_index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        " Add", action=f"screen.add({self.current_song_index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        " Delete", action=f"screen.remove({self.current_song_index})", classes="actions-cell"
                    )
            yield Static("", classes="spacer")
            yield Static("#", classes="header-cell")
            yield Static("Title", classes="header-cell")
            yield Static("Artist", classes="header-cell")
            yield Static("Actions", classes="header-cell")
            for index, song in enumerate(self.songbook.songs):
                yield Static(str(index + 1), classes="cell")
                yield Static(song.title, classes="cell")
                yield Static(song.artist or "", classes="cell")
                with Horizontal(classes="actions-container"):
                    # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
                    # yield Static(f"[@click=down({index})]  [/]", classes="actions-cell")
                    # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
                    yield ActionButton(
                        "", action=f"screen.up({index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        "", action=f"screen.down({index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        " ", action=f"screen.add({index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        "", action=f"screen.remove({index})", classes="actions-cell"
                    )

    def action_up(self, index: int):
        print("action_up")
        if index == 0:
            return
        song = self.songbook.songs.pop(index)
        self.songbook.songs.insert(index - 1, song)
        # self.recompose()
        # recompose doesn't work, hacky close and reopen
        self.app.pop_screen()
        self.app.push_screen(SongbookOverviewModal(self.songbook, self.current_song_index))
        print([s.title for s in self.songbook.songs])

    def action_down(self, index: int):
        print("action_down")
        if index == len(self.songbook.songs) - 1:
            return
        song = self.songbook.songs.pop(index)
        self.songbook.songs.insert(index + 1, song)
        # self.recompose()
        self.app.pop_screen()
        self.app.push_screen(SongbookOverviewModal(self.songbook, self.current_song_index))
        print([s.title for s in self.songbook.songs])

    def action_add(self, index: int):
        self.app.push_screen(SongOverviewModal(self.songs, self.songbook, self.current_song_index))

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
            self.app.push_screen(SongbookOverviewModal(self.songbook, self.current_song_index))
        print([s.title for s in self.songbook.songs])
