from asyncio import sleep

from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Label, ProgressBar, LoadingIndicator

from backend import service
from backend.dto import SongDTO, SongbookDTO


class LoadingSplash(ModalScreen):
    """The loading splash screen for the Songbook TUI."""

    songs: dict[int, SongDTO]
    songbooks: dict[str, SongbookDTO]

    async def on_mount(self) -> None:
        """Run when the screen is mounted."""

        progress_bar = self.query_one(ProgressBar)
        progress_bar.update(total=2)
        self.songs = await service.get_songs()
        progress_bar.advance(1)
        self.songbooks = await service.get_songbooks(self.songs)
        progress_bar.advance(1)
        # await sleep(1)
        self.dismiss((self.songs, self.songbooks))

    def compose(self) -> ComposeResult:
        """Compose the loading splash screen."""

        yield Label("󰎆 Songbooks")
        yield ProgressBar()
        yield LoadingIndicator()
