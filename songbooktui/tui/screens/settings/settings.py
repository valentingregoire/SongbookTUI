from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Pretty

from backend.model import Settings


class SettingsScreen(Screen):
    settings: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Pretty(self.settings)
