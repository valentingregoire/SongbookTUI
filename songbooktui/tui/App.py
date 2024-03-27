from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Static


class TimeDisplay(Static):
    """A widget that displays the current time."""

    pass


class Stopwatch(Static):

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class SongbookApp(App):
    """The main application class for the Songbook TUI."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]

    def compose(self) -> ComposeResult:
        """Compose the application."""
        yield Header()
        yield Footer()
        yield Stopwatch()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = SongbookApp()
    app.run()
