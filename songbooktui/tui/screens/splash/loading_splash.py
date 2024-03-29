from asyncio import sleep

from textual import work
from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Label, ProgressBar, LoadingIndicator

from backend import service
from backend.dto import SongDTO, SongbookDTO


class LoadingSplash(Screen):
    """The loading splash screen for the Songbook TUI."""

    CSS_PATH = "loading_splash.tcss"

    songs: dict[int, SongDTO]
    songbooks: dict[str, SongbookDTO]
    status: reactive[str] = reactive("Loading...")

    async def on_mount(self) -> None:
        self.fetch_data()

    def compose(self) -> ComposeResult:
        """Compose the loading splash screen."""

        # with Center():
        #     with Middle():
        #         yield Label("󰎆 Songbooks")
        #         yield ProgressBar(total=2, show_eta=False, show_percentage=False)
        #         yield LoadingIndicator()
        #         yield Label(self.status)
        yield Label("󰎆 Songbooks")
        yield ProgressBar(total=2, show_eta=False, show_percentage=False)
        yield LoadingIndicator()
        yield Label(self.status)

    async def update_progress(self) -> None:
        progress_bar = self.query_one(ProgressBar)
        progress_bar.advance(1)
        await sleep(1)
        if progress_bar.progress == 2:
            self.status = reactive("Done!")
            await sleep(1)
            self.dismiss((self.songs, self.songbooks))

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
