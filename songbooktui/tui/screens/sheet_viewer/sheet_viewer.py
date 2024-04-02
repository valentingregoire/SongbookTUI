from rich.console import RenderableType
from textual._easing import DEFAULT_EASING
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Static, Button
from textual.widgets._header import HeaderTitle

from backend.dto import SongDTO, SongbookDTO


class SheetViewer(Screen):

    CSS_PATH = "sheet_viewer.tcss"
    BINDINGS = [("q", "request_quit", "Quit")]

    songbook: SongbookDTO
    current_song_index: reactive[int] = reactive(0, recompose=True)
    current_page_index: reactive[int] = reactive(0, recompose=True)
    current_song: reactive[SongDTO] = reactive(None)
    current_page: reactive[str] = reactive("some content yo")

    def compute_current_song(self) -> SongDTO:
        print("compute current song: " + str(self.current_song_index))
        return self.songbook.songs[self.current_song_index]

    def compute_current_page(self) -> str:
        print("compute current song: " + str(self.current_page_index))
        return self.current_song.pages[self.current_page_index]

    # def watch_current_page_index(self, value: int) -> None:
    #     print("watch current page index: " + str(value))
        # self.query_one("#viewer").content = f"{self.current_song_index} - {self.current_page_index}/{len(self.current_song.pages)}"
        # self.query_one("#viewer").content = f"{self.current_song_index} - {self.current_page_index}"


    def __init__(self, songbook: SongbookDTO) -> None:
        self.songbook = songbook
        # self.current_song_index = 0
        # self.current_page_index = 0
        super().__init__()

    def on_mount(self) -> None:
        self.title = "blabls"
        self.sub_title = "sup bro"
        self.styles.animate("opacity", value=1, duration=0.3, easing="out_circ")

    def compose(self) -> ComposeResult:
        yield Static(self.current_page, id="viewer")
        yield Button("PS", id="btn_prev_song", classes="side")
        # yield Button("Menu", id="btn_menu")
        yield Button("NS", id="btn_next_song", classes="side")
        yield Button("PP", id="btn_prev_page", classes="side")
        yield Button("NP", id="btn_next_page", classes="side")
        yield Header()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        # self.query_one(Static).content = event.button.id
        #  = f"{self.current_song_index - self.current_page_index/len(self.current_song.pages)}"
        # header = self.query_one(Header)
        # header.query_one(HeaderTitle).text = reactive("button pressed")
        # self.title = "button pressed"
        # self.sub_title = "sup2"
        if event.button.id == "btn_prev_song":
            self.current_song_index -= 1
        elif event.button.id == "btn_next_song":
            self.current_song_index += 1
        elif event.button.id == "btn_prev_page":
            self.current_page_index -= 1
        elif event.button.id == "btn_next_page":
            self.current_page_index += 1
