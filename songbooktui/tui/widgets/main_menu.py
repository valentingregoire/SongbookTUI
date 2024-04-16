from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button


class MainMenu(Vertical):
    CSS_PATH = "main_menu.tcss"
    DEFAULT_CSS = """
        MainMenu {
            # layer: menu;
            # dock: left;
            # height: 100%;
            # width: 20%;
        }
    """

    def compose(self) -> ComposeResult:
        with Center():
            # yield Static(utils.TITLE)
            yield Button("󱍙  Songbooks", id="btn_songbooks", variant="primary")
            yield Button("󰎈  Songs", id="btn_songs")
            yield Button("󰒓  Options", id="btn_options")
            yield Button.error("󰗼  Quit", id="btn_quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_quit":
            self.app.exit()
