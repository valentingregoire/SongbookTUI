from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from backend.dto import SongbookDTO, SongDTO
from tui.screens.sheet_viewer.sheet_viewer import SheetViewer
from tui.screens.splash.loading_splash import LoadingSplash

DEFAULT_SONGBOOK = "2024"


class SongbookApp(App):
    """The main application class for the Songbook TUI."""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "exit", "Quit")
    ]

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
            self.push_screen(SheetViewer(songs=self.songs, songbook=songbooks.get(DEFAULT_SONGBOOK)))

        self.push_screen(LoadingSplash(), set_loaded_data)

    #Application wide actions!
    def action_ok(self) -> None:
        self.dismiss()

    def action_exit(self) -> None:
        self.app.exit()

if __name__ == "__main__":
    app = SongbookApp()
    app.run()
