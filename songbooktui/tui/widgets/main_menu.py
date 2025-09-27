from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Static

from backend import service
from backend.consts import BASE_LOCATION
from backend.dto import SongbookDTO, SongDTO
from backend.model import Settings
from git import GitCommandError, Repo
from tui import utils
from tui.screens.settings.settings import SettingsScreen
from tui.screens.songbooks.songbooks_screen import SongbooksScreen
from tui.screens.songs.songs_screen import SongsScreen
from tui.utils import ok, cancel, VERSION


class MainMenu(Vertical):
    CSS_PATH = "main_menu.tcss"

    songs: dict[int, SongDTO]
    songbooks: dict[int, SongbookDTO]
    settings: Settings
    pull_result: str | None = None

    def __init__(
        self,
        title: str,
        songs: dict[int, SongDTO],
        songbooks: dict[int, SongbookDTO],
        settings: Settings,
        id: str | None = None,
        classes: str | None = None,
        *args,
    ) -> None:
        super().__init__(id=id, classes=classes, *args)
        self.title = title
        self.songs = songs
        self.songbooks = songbooks
        self.settings = settings

    def compose(self) -> ComposeResult:
        with Center():
            yield Static(
                f"[b]{utils.SONGBOOK} {self.title}[/b]", classes="center-middle"
            )
            yield Button(f"{utils.SONGBOOK} Songbooks", id="btn_songbooks")
            yield Button(f"{utils.SONG} Songs", id="btn_songs")
            yield Button("󰒓  Settings", id="btn_settings")
            yield Button("󰓂 Pull", id="btn_pull")
            yield Button("󰚰  Update", id="btn_update")
            yield Button.error("󰗼  Quit", id="btn_quit")
            yield Static(f"v{VERSION}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        async def fallback_songbooks_screen(songbook_id: int) -> None:
            while self.app.screen_stack[-1].id != "sheet_viewer":
                self.app.pop_screen()
            self.screen.dismiss(songbook_id)

        if event.button.id == "btn_songbooks":
            await self.app.push_screen(
                SongbooksScreen(
                    songs=self.songs, songbooks=self.songbooks, settings=self.settings
                ),
                fallback_songbooks_screen,
            )
        elif event.button.id == "btn_songs":
            await self.app.push_screen(SongsScreen(self.songs))
        elif event.button.id == "btn_settings":

            def fallback(data: Settings) -> None:
                self.settings = data
                self.notify(ok(" Settings saved."))

            await self.app.push_screen(
                SettingsScreen(self.settings, songbooks=self.songbooks), fallback
            )
        elif event.button.id == "btn_pull":
            await self.pull_updates()
        elif event.button.id == "btn_update":
            success = await service.update()
            if success:
                self.app.notify(ok(" Update successful!"))
                self.app.exit(message="Update successful, restart the app.")
            else:
                self.app.notify(cancel(" Update failed!"))
        elif event.button.id == "btn_quit":
            self.app.exit()

    async def pull_updates(self) -> None:
        """Pull updates from the repository."""

        self.log("Pulling updates from the repository.")
        try:
            repo = Repo(BASE_LOCATION)
            pull_result = repo.git.pull()
            self.log(pull_result)
            self.pull_result = pull_result
            self.notify(ok(f" {pull_result}."))
        except GitCommandError as e:
            self.log("Error pulling updates from the repository.")
            self.log(e)
            self.pull_result = "Error pulling updates from the repository."
            self.notify(cancel(f" {self.pull_result}."))
        finally:
            self.settings.pull_result = self.pull_result
