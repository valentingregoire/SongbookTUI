from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import SelectionList
from textual.widgets.selection_list import Selection

from backend.dto import SongbookDTO, SongDTO
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import TopBar, RightFloat


class SongOverviewModal(ModalScreen):
    BINDINGS = [
        ("q", "pop_screen", "Quit"),
    ]

    songs: dict[int, SongDTO]
    songbook: SongbookDTO | None
    current_song_index: int | None

    def __init__(
        self,
        songs: dict[int, SongDTO],
        songbook: SongbookDTO | None,
        current_song_index: int | None,
    ) -> None:
        self.songs = songs
        self.songbook = songbook
        self.current_song_index = current_song_index
        super().__init__()

    def compose(self) -> ComposeResult:
        with TopBar():
            with RightFloat():
                yield ActionButton("", id="btn_close", action="pop_screen")
        yield SelectionList[int](
            *[
                Selection(
                    s.full_title,
                    i,
                    s in self.songbook.songs if self.songbook else False,
                )
                for i, s in self.songs.items()
            ]
        )
