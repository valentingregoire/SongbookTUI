from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button

from backend.dto import SongbookDTO
from backend.model import Settings
from tui.screens.settings.settings import SettingsScreen


class MainMenu(Vertical):
    CSS_PATH = "main_menu.tcss"

    songbooks: dict[int, SongbookDTO]
    settings: Settings

    def __init__(
        self,
        songbooks: dict[int, SongbookDTO],
        settings: Settings,
        id: str | None = None,
        classes: str | None = None,
        *args,
    ) -> None:
        self.songbooks = songbooks
        self.settings = settings
        super().__init__(id=id, classes=classes, *args)

    def compose(self) -> ComposeResult:
        with Center():
            # yield Static(utils.TITLE)
            yield Button("󱍙  Songbooks", id="btn_songbooks", variant="primary")
            yield Button("󰎈  Songs", id="btn_songs")
            yield Button("󰒓  Settings", id="btn_settings")
            yield Button.error("󰗼  Quit", id="btn_quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_settings":
            self.app.push_screen(
                SettingsScreen(self.settings, songbooks=self.songbooks)
            )
        elif event.button.id == "btn_quit":
            self.app.exit()
