from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button


class MainMenu(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Button("󱍙  Songbooks", id="btn_songbooks", variant="primary")
        yield Button("󰎈  Songs", id="btn_songs")
        yield Button("󰒓  Options", id="btn_options")
        yield Button.error("󰗼  Quit", id="btn_quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_quit":
            self.app.exit()
