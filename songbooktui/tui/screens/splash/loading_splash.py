from asyncio import sleep

from art import text2art
from textual import work
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import ProgressBar, Static

from backend import service
from backend.dto import SongDTO, SongbookDTO


class LoadingSplash(Screen):
    """The loading splash screen for the Songbook TUI."""

    CSS_PATH = "loading_splash.tcss"
    BINDINGS = [("q", "request_quit", "Quit")]

    songs: dict[int, SongDTO]
    songbooks: dict[str, SongbookDTO]

    async def on_mount(self) -> None:
        self.fetch_data()

    def compose(self) -> ComposeResult:
        """Compose the loading splash screen."""
        title = text2art("Songbooks", font="doom")
        with Center():
            yield Static(title)
        with Center():
            yield ProgressBar(total=2, show_eta=False, show_percentage=False)

    async def update_progress(self) -> None:
        progress_bar = self.query_one(ProgressBar)
        progress_bar.advance(1)
        if progress_bar.progress == 2:
            progress_bar.styles.animate(
                "opacity", value=0, duration=0.3, easing="out_quint"
            )
            # await sleep(1)
            self.styles.animate("opacity", value=0, duration=0.3, easing="out_quint")
            self.dismiss((self.songs, self.songbooks))

    def action_request_quit(self) -> None:
        """Quit the application."""
        # self.push_screen(MainMenu())
        self.app.exit()

    @work
    async def fetch_data(self) -> None:
        """Get the songs."""

        songs = await service.get_songs()
        self.songs = songs
        await self.update_progress()
        await self.get_songbooks(songs)
        await self.update_progress()

    async def get_songbooks(self, songs: dict[int, SongDTO]) -> None:
        """Get the songbooks."""

        self.songbooks = await service.get_songbooks(songs)
        await self.update_progress()
