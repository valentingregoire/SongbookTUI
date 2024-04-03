from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Markdown,
    ContentSwitcher,
    Static,
    Label,
)

from backend.dto import SongDTO, SongbookDTO, PageDTO
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import LeftFloat, RightFloat, TopBar, CenterFloat
from tui.widgets.progress_bar import InlineVerticalProgressBar
from tui.widgets.top_bar import PageInfo, SongInfo


class SheetViewer(Screen):

    CSS_PATH = "sheet_viewer.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
        ("n", "next_song", "Next Song"),
    ]

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

    # def watch_current_page_index(self, value: int) -> None:
    #     print("watch current page index: " + str(value))
    # self.query_one("#viewer").content = f"{self.current_song_index} - {self.current_page_index}/{len(self.current_song.pages)}"
    # self.query_one("#viewer").content = f"{self.current_song_index} - {self.current_page_index}"

    # def watch_current_song(self, song: SongDTO) -> None:
    #     self.query_one(ContentSwitcher).current = f"viewer_{song.file_type.name.lower()}"

    def __init__(self, songbook: SongbookDTO) -> None:
        self.songbook = songbook
        # self.current_song_index = 0
        # self.current_page_index = 0
        super().__init__()

    def on_mount(self) -> None:
        self.styles.animate("opacity", value=1, duration=0.3, easing="out_circ")

    def compose(self) -> ComposeResult:
        # with VerticalScroll():
        with ContentSwitcher(initial=self.current_viewer):
            # yield Static(self.current_page.content, id="viewer_txt")
            yield Label(self.current_page.content, id="viewer_txt")
            yield Markdown(
                self.current_page.content,
                id="viewer_md",
            )

        with TopBar():
            with LeftFloat():
                yield ActionButton("  ", "screen.prev_song", id="btn_prev_song")
            with CenterFloat():
                yield Static(self.current_song.title, id="lbl_song_title")
            with RightFloat():
                yield InlineVerticalProgressBar(self.current_song_index + 1, len(self.songbook.songs))
                yield PageInfo(
                    self.current_page_index + 1, len(self.current_song.pages)
                )
                yield SongInfo(self.current_song_index + 1, len(self.songbook.songs))
                yield ActionButton("  ", "screen.next_song", id="btn_next_song")

    def action_prev_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (
            self.current_song_index + len(self.songbook.songs) - 1
        ) % len(self.songbook.songs)

    def action_next_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (self.current_song_index + 1) % len(
            self.songbook.songs
        )

    def action_prev_page(self) -> None:
        if self.current_page_index > 0:
            self.current_page_index -= 1
        else:
            self.action_prev_song()
            self.current_page_index = len(self.current_song.pages) - 1

        self.current_page_index -= 1

    def action_next_page(self) -> None:
        if self.current_page_index < len(self.current_song.pages) - 1:
            self.current_page_index += 1
        else:
            self.action_next_song()
