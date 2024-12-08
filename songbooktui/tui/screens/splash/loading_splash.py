from backend import service
from backend.consts import BASE_LOCATION
from backend.dto import SongbookDTO, SongDTO
from backend.model import Settings
from git import Repo
from textual import work
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import ProgressBar, Static
from tui import utils


class LoadingSplash(Screen):
    """The loading splash screen for the Songbook TUI."""

    CSS_PATH = "loading_splash.tcss"

    songs: dict[int, SongDTO]
    songbooks: dict[int, SongbookDTO]
    settings: Settings
    pull_result: str | None = None

    async def on_mount(self) -> None:
        self.fetch_data()

    def compose(self) -> ComposeResult:
        """Compose the loading splash screen."""
        with Center():
            yield Static(utils.TITLE)
        with Center():
            yield ProgressBar(total=3, show_eta=False, show_percentage=False)

    async def update_progress(self) -> None:
        progress_bar = self.query_one(ProgressBar)
        progress_bar.advance(1)
        if progress_bar.progress == 4:
            progress_bar.styles.animate(
                "opacity", value=0, duration=1.3, easing="out_quint"
            )
            # await sleep(1)
            self.styles.animate("opacity", value=0, duration=0.3, easing="out_quint")
            self.dismiss((self.songs, self.songbooks, self.settings))

    @work
    async def fetch_data(self) -> None:
        """Get the songs."""

        await self.pull_updates()
        await self.get_songs()
        await self.get_songbooks()
        await self.get_settings()

    async def pull_updates(self) -> None:
        """Pull updates from the repository."""

        self.log("Pulling updates from the repository.")
        repo = Repo(BASE_LOCATION)
        pull_result = repo.git.pull()
        self.log(pull_result)
        self.pull_result = pull_result
        await self.update_progress()

    async def get_songs(self) -> None:
        """Get the songs."""

        self.songs = await service.get_songs()
        await self.update_progress()

    async def get_songbooks(self) -> None:
        """Get the songbooks."""

        self.songbooks = await service.get_songbooks(self.songs)
        await self.update_progress()

    async def get_settings(self) -> None:
        """Get the settings."""

        self.settings = await service.get_settings()
        self.settings.pull_result = self.pull_result
        await self.update_progress()
