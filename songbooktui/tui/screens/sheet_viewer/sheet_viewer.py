from rich.console import RenderableType
from textual._easing import DEFAULT_EASING
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Static, Button

from backend.dto import SongDTO, SongbookDTO


class SheetViewer(Screen):

    CSS_PATH = "sheet_viewer.tcss"

    songbook: reactive[SongbookDTO]
    song: reactive[SongDTO]
    current_page_index: reactive[int] = 0

    def __init__(self, songbook: SongbookDTO) -> None:
        self.songbook = reactive(songbook)
        self.song = reactive(songbook.songs[0])
        super().__init__()

    def on_mount(self) -> None:
        self.styles.animate("opacity", value=1, duration=0.3, easing="out_circ")

    def compose(self) -> ComposeResult:
        yield Static("Viewer", id="viewer")
        yield Button("PS", id="btn_prev_song", classes="side")
        yield Button("Menu", id="btn_menu")
        yield Button("NS", id="btn_next_song", classes="side")
        yield Button("PP", id="btn_prev_page", classes="side")
        yield Button("NP", id="btn_next_page", classes="side")
        yield Header()

