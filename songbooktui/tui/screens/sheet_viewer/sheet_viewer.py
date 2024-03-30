from rich.console import RenderableType
from textual._easing import DEFAULT_EASING
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Static, Button

from backend.dto import SongDTO, SongbookDTO


class SheetViewer(Screen):

    CSS_PATH = "sheet_viewer.tcss"
    BINDINGS = [("q", "request_quit", "Quit")]

    songbook: SongbookDTO
    current_song_index: int = 0
    current_page_index: int = 0
    content: reactive[str] = reactive("some content", recompose=True)

    def __init__(self, songbook: SongbookDTO) -> None:
        self.songbook = songbook
        super().__init__()

    def on_mount(self) -> None:
        self.styles.animate("opacity", value=1, duration=0.3, easing="out_circ")

    def compose(self) -> ComposeResult:
        yield Static(self.content, id="viewer")
        yield Button("PS", id="btn_prev_song", classes="side")
        # yield Button("Menu", id="btn_menu")
        yield Button("NS", id="btn_next_song", classes="side")
        yield Button("PP", id="btn_prev_page", classes="side")
        yield Button("NP", id="btn_next_page", classes="side")
        yield Header()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        # self.query_one(Static).content = event.button.id
        self.content = f"🌐 event.button.id"
        if event.button.id == "btn_prev_song":
            self.current_song_index -= 1
        elif event.button.id == "btn_next_song":
            self.current_song_index += 1
        elif event.button.id == "btn_prev_page":
            self.current_page_index -= 1
        elif event.button.id == "btn_next_page":
            self.current_page_index += 1
