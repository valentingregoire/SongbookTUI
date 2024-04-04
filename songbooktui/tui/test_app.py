from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Markdown

from backend.dto import SongbookDTO, SongDTO
from tui.screens.splash.loading_splash import LoadingSplash

DEFAULT_SONGBOOK = "2024"


class SongbookTestApp(App):
    """The main application class for the Songbook TUI."""

    CSS = """
    Markdown {
        width: 100%;
        height: 100%;
    }
    """
    BINDINGS = [("q", "request_quit", "Quit")]
    # MODES = {
    #     "splash": LoadingSplash,
    #     "viewer": SheetViewer,
    # }

    songs: dict[int, SongDTO]
    songbooks: dict[str, SongbookDTO]

    def on_mount(self) -> None:
        """Run when the app is mounted."""

        def set_loaded_data(
            data: tuple[dict[int, SongDTO], dict[str, SongbookDTO]]
        ) -> None:
            """Fallback function to set the loaded data."""
            songs, songbooks = data
            self.songs = songs
            self.songbooks = songbooks
            # self.switch_mode("viewer")

            self.query_one(Markdown).update(
                self.songbooks[DEFAULT_SONGBOOK].songs[0].pages[1]
            )

        self.push_screen(LoadingSplash(), set_loaded_data)

    def compose(self) -> ComposeResult:
        """Compose the application."""
        yield Header()
        yield Footer()
        yield Markdown("Loading...", id="viewer_md")
        # yield MainMenu()

    def action_request_quit(self) -> None:
        """Quit the application."""
        # self.push_screen(MainMenu())
        self.app.exit()


if __name__ == "__main__":
    app = SongbookTestApp()
    app.run()
