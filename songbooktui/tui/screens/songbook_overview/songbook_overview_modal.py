from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Static

from backend.dto import SongbookDTO
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import TopBar, LeftFloat, RightFloat, CenterFloat


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
    BINDINGS = [
        ("q", "pop_screen", "Quit"),
    ]
    songbook: SongbookDTO
    current_song_index: int

    def __init__(
        self,
        songbook: SongbookDTO,
        current_song_index: int,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.songbook = songbook
        self.current_song_index = current_song_index

    def compose(self) -> ComposeResult:
        with Grid(id="table"):
            with TopBar():
                with LeftFloat():
                    pass
                with CenterFloat():
                    yield Static(self.songbook.name)
                with RightFloat():
                    yield ActionButton("", id="btn_close", action="pop_screen")
            yield Static("#", classes="header-cell")
            yield Static("Title", classes="header-cell")
            yield Static("Artist", classes="header-cell")
            yield Static("Actions", classes="header-cell")
            for index, song in enumerate(self.songbook.songs):
                yield Static(str(index + 1), classes="cell")
                yield Static(song.title, classes="cell")
                yield Static(song.artist, classes="cell")
                with Horizontal(classes="actions-container"):
                    # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
                    # yield Static(f"[@click=down({index})]  [/]", classes="actions-cell")
                    # yield Static(f"[@click=up({index})]  [/]", classes="actions-cell")
                    yield ActionButton(
                        "", action=f"up({index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        "", action=f"down({index})", classes="actions-cell"
                    )
                    yield ActionButton(
                        "", action=f"remove({index})", classes="actions-cell"
                    )
