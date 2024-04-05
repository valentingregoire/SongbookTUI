from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from backend.dto import SongbookDTO
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import TopBar, LeftFloat, RightFloat, CenterFloat
from tui.widgets.songbook_overview_table import SongbookOverviewTable


class SongbookOverviewModal(ModalScreen):
    CSS_PATH = "songbook_overview_modal.tcss"
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
        # yield SongbookOverviewTable(self.songbook, self.current_song_index)
        with Vertical():
            with TopBar():
                with LeftFloat():
                    pass
                with CenterFloat():
                    yield Static(self.songbook.name)
                    pass
                with RightFloat():
                    yield ActionButton("", id="btn_close", action="pop_screen")
            for index, song in enumerate(self.songbook.songs):
                yield Static(f"{index} - {song.title} - {song.artist}")

            yield Static("This is some text.")
