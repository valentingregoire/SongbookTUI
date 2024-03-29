from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, Button

from backend.dto import SongbookDTO, SongDTO
from tui.screens.loading_splash import LoadingSplash
from tui.screens.main_menu import MainMenu


class SongbookApp(App):
    """The main application class for the Songbook TUI."""

    CSS_PATH = "app.tcss"
    BINDINGS = [("q", "request_quit", "Quit")]

    songs: reactive[dict[int, SongDTO]]
    songbooks: reactive[dict[str, SongbookDTO]]

    def on_mount(self) -> None:
        """Run when the app is mounted."""

        def set_loaded_data(data: tuple[dict[int, SongDTO], dict[str, SongbookDTO]]) -> None:
            """Fallback function to set the loaded data."""
            songs, songbooks = data
            self.songs = songs
            self.songbooks = songbooks

        self.push_screen(LoadingSplash(), set_loaded_data)

    def compose(self) -> ComposeResult:
        """Compose the application."""
        yield Header()
        yield Footer()
        yield MainMenu()

    def action_request_quit(self) -> None:
        """Quit the application."""
        self.push_screen(MainMenu())


if __name__ == "__main__":
    app = SongbookApp()
    app.run()
