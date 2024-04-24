from textual.app import App

from backend.dto import SongbookDTO, SongDTO
from backend.model import Settings
from tui.screens.sheet_viewer.sheet_viewer import SheetViewer
from tui.screens.splash.loading_splash import LoadingSplash

DEFAULT_SONGBOOK = "2024"


class SongbookApp(App):
    """The main application class for the Songbook TUI."""

    CSS_PATH = "app.tcss"
    BINDINGS = [("q", "exit", "Quit")]

    songs: dict[int, SongDTO]
    songbooks: dict[str, SongbookDTO]
    settings: Settings = Settings()

    # def compose(self) -> ComposeResult:
    #     """Compose the main application."""
    #     # yield MainMenu(settings=self.settings, id="menu", classes="hidden").data_bind(
    #     #     disabled=SheetViewer.menu_shown
    #     # )

    def on_mount(self) -> None:
        """Run when the app is mounted."""

        def set_loaded_data(
            data: tuple[dict[int, SongDTO], dict[int, SongbookDTO], Settings],
        ) -> None:
            """Fallback function to set the loaded data."""
            songs, songbooks, settings = data
            self.songs = songs
            self.songbooks = songbooks
            self.settings = settings
            self.push_screen(
                SheetViewer(
                    songs=self.songs,
                    songbook=songbooks.get(settings.default_songbook),
                    songbooks=songbooks,
                    settings=settings,
                )
            )

        self.push_screen(LoadingSplash(), set_loaded_data)

    # Application wide actions!
    def action_ok(self) -> None:
        self.screen.dismiss()

    def action_cancel(self) -> None:
        self.pop_screen()

    def action_exit(self) -> None:
        self.app.exit()


if __name__ == "__main__":
    app = SongbookApp()
    app.run()
