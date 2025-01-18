from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import SelectionList
from textual.widgets.selection_list import Selection

from backend.dto import SongbookDTO, SongDTO
from tui.utils import cancel, ok, DEFAULT_BINDINGS
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import ActionsBar


class SongOverviewModal(ModalScreen):
    CSS_PATH = "song_overview_modal.tcss"
    BINDINGS = DEFAULT_BINDINGS

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
        song_list = self.songbook.songs + [
            song for song in self.songs.values() if song not in self.songbook.songs
        ]
        selection = SelectionList[SongDTO](
            *[
                Selection(
                    song.full_title,
                    song,
                    song in self.songbook.songs if self.songbook else False,
                )
                for song in song_list
            ],
            id="selection-list",
        )
        selection.styles.height = self.app.size.height - 4
        yield selection
        with ActionsBar():
            yield ActionButton(cancel(), action="pop_screen", classes="btn-link error")
            yield ActionButton(ok(), action="screen.ok", classes="btn-link success")

    def action_ok(self) -> None:
        selection = self.query_one(SelectionList[int])
        self.dismiss(selection.selected)
