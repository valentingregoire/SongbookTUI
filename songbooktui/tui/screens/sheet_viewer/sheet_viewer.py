from numba import jit
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Markdown,
    ContentSwitcher,
    Static,
    Label,
)

from backend.dto import SongDTO, SongbookDTO, PageDTO
from tui.screens.songbook_overview.songbook_overview_modal import SongbookOverviewModal
from tui.utils import ok
from tui.widgets.action_button import ActionButton
from tui.widgets.bottom_bar import PageInfo
from tui.widgets.containers import LeftFloat, RightFloat, TopBar, CenterFloat, BottomBar
from tui.widgets.progress_bar import InlineVerticalProgressBar
from tui.widgets.top_bar import SongInfo


class SheetViewer(Screen):

    CSS_PATH = "sheet_viewer.tcss"
    BINDINGS = [
        ("o", "show_songbook_overview", "  Overview"),
        ("q", "request_quit", "Quit"),
    ]

    songs: dict[int, SongDTO]
    songbook: SongbookDTO
    current_song_index: reactive[int] = reactive(0, recompose=True)
    current_page_index: reactive[int] = reactive(0, recompose=True)
    current_song: reactive[SongDTO] = reactive(None)
    current_page: reactive[PageDTO] = reactive(None)
    current_viewer: reactive[str] = reactive("viewer_txt")

    def compute_current_song(self) -> SongDTO:
        return self.songbook.songs[self.current_song_index]

    def compute_current_page(self) -> str:
        return self.current_song.pages[self.current_page_index]

    def compute_current_viewer(self) -> str:
        return f"viewer_{self.current_page.file_type}"

    def __init__(self, songs: dict[int, SongDTO], songbook: SongbookDTO) -> None:
        self.songs = songs
        self.songbook = songbook
        super().__init__()

    def on_mount(self) -> None:
        self.styles.animate("opacity", value=1, duration=0.3, easing="out_circ")

    # @jit
    def compose(self) -> ComposeResult:
        with Vertical(classes="h-full w-full top-center", id="viewer-container"):
            with ContentSwitcher(initial=self.current_viewer):
                with VerticalScroll(id="viewer_txt"):
                    yield Static(self.current_page.content, classes="w-auto")
                with VerticalScroll(id="viewer_md"):
                    yield Markdown(
                        self.current_page.content,
                        # id="viewer_md",
                    )
        with TopBar():
            with LeftFloat():
                yield ActionButton("  ", "screen.prev_song", classes="p-r-1 m-0")
                yield Static(self.current_song.full_title, classes="text-bold")
            with RightFloat():
                yield InlineVerticalProgressBar(
                    self.current_song_index + 1, self.songbook.size
                )
                yield SongInfo(self.current_song_index + 1, self.songbook.size)
                yield ActionButton("  ", "screen.next_song", classes="p-l-1 m-0")
        with BottomBar():
            with LeftFloat():
                yield ActionButton("  ", "screen.prev_page", classes="p-r-1 m-0")
                next_song_index = (self.current_song_index + 1) % self.songbook.size
                yield Static(self.songbook.songs[next_song_index].full_title, classes="text-bold")
            with RightFloat():
                yield ActionButton(
                    "  Overview",
                    "screen.show_songbook_overview",
                )
                yield InlineVerticalProgressBar(
                    self.current_page_index + 1, len(self.current_song.pages)
                )
                yield PageInfo(
                    self.current_page_index + 1, len(self.current_song.pages),
                )
                yield ActionButton("  ", "screen.next_page", classes="p-l-1 m-0")

    def action_show_songbook_overview(self) -> None:
        def fallback(data: tuple[SongbookDTO, int]) -> None:
            songbook, current_song_index = data
            self.songbook = songbook
            self.current_song_index = current_song_index
            self.current_page_index = 0
            self.notify(ok(" Songbook updated."))

        self.app.push_screen(
            SongbookOverviewModal(self.songs, self.songbook, self.current_song_index),
            fallback,
        )

    def action_prev_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (
            self.current_song_index + self.songbook.size - 1
        ) % self.songbook.size

    def action_next_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (self.current_song_index + 1) % self.songbook.size

    def action_prev_page(self) -> None:
        if self.current_page_index > 0:
            self.current_page_index -= 1
        else:
            self.action_prev_song()
            self.current_page_index = len(self.current_song.pages) - 1

    def action_next_page(self) -> None:
        if self.current_page_index < len(self.current_song.pages) - 1:
            self.current_page_index += 1
        else:
            self.action_next_song()
