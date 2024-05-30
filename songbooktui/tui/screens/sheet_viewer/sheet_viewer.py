import dataclasses

from rich.markdown import Markdown
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    ContentSwitcher,
    Static,
    Label,
)

from backend.dto import PageDTO, SongbookDTO, SongDTO
from backend.model import Settings, FileType
from tui import sheet_parser
from tui.screens.settings.settings import SettingsScreen
from tui.screens.songbook_overview.songbook_overview_modal import SongbookOverviewModal
from tui.utils import ok
from tui.widgets.action_button import ActionButton
from tui.widgets.bottom_bar import PageInfo
from tui.widgets.containers import BottomBar, LeftFloat, RightFloat, TopBar
from tui.widgets.main_menu import MainMenu
from tui.widgets.progress_bar import InlineVerticalProgressBar
from tui.widgets.top_bar import SongInfo


class SheetViewer(Screen):
    CSS_PATH = "sheet_viewer.tcss"
    BINDINGS = [
        ("l", "next_page", "Next Page"),
        ("h", "prev_page", "Previous Page"),
        ("k", "next_song", "Next Song"),
        ("j", "prev_song", "Previous Song"),
        ("o", "show_songbook_overview", "  Overview"),
        ("m", "toggle_menu", "󰍜 Menu"),
        ("s", "settings", "Settings"),
        ("q", "request_quit", "Quit"),
    ]

    songs: dict[int, SongDTO]
    songbook: SongbookDTO
    settings: Settings

    current_song_index: reactive[int] = reactive(0, recompose=True)
    current_page_index: reactive[int] = reactive(0, recompose=True)
    current_song: reactive[SongDTO] = reactive(None)
    current_page: reactive[PageDTO] = reactive(None)
    current_viewer: reactive[str] = reactive("viewer_txt")
    menu_shown: bool = False

    def compute_current_song(self) -> SongDTO:
        return self.songbook.songs[self.current_song_index]

    def compute_current_page(self) -> str:
        return self.current_song.pages[self.current_page_index]

    def compute_current_viewer(self) -> str:
        return f"viewer_{self.current_page.file_type}"

    def __init__(
        self,
        songs: dict[int, SongDTO],
        songbook: SongbookDTO,
        songbooks: dict[int, SongbookDTO],
        settings: Settings,
    ) -> None:
        self.songs = songs
        self.songbook = songbook
        self.songbooks = songbooks
        self.settings = settings
        super().__init__(id="sheet_viewer")

    def on_mount(self) -> None:
        self.auto_paginate()
        self.styles.animate("opacity", value=1, duration=1.3, easing="out_circ")

    def compose(self) -> ComposeResult:
        with Vertical(classes="h-full w-full top-center", id="viewer-container"):
            with ContentSwitcher(initial=self.current_viewer):
                with VerticalScroll(id="viewer_txt"):
                    yield Label(
                        sheet_parser.markup(self.current_page.content),
                        # self.current_page.content,
                        classes="w-auto",
                        markup=True,
                    )
                with VerticalScroll(id="viewer_md"):
                    md = Markdown(markup=self.current_page.content)
                    yield Static(md, id="stc_md")
        with TopBar():
            with LeftFloat():
                yield ActionButton("󰍜 ", "screen.toggle_menu", classes="w-auto")
                yield ActionButton("  ", "screen.prev_song", classes="p-r-1 m-0")
                yield Static(self.current_song.full_title, classes="text-bold")
            with RightFloat():
                yield InlineVerticalProgressBar(
                    self.current_song_index + 1, self.songbook.size
                )
                yield SongInfo(self.current_song_index + 1, self.songbook.size)
                yield ActionButton("  ", "screen.next_song", classes="p-l-1 m-0")
        with BottomBar():
            with LeftFloat():
                yield ActionButton("  ", "screen.prev_page", classes="p-r-1 m-0")
                next_song_index = (self.current_song_index + 1) % self.songbook.size
                yield Static(
                    self.songbook.songs[next_song_index].full_title, classes="text-bold"
                )
            with RightFloat():
                yield ActionButton(
                    "  Overview",
                    "screen.show_songbook_overview",
                    classes="center-middle",
                )
                yield InlineVerticalProgressBar(
                    self.current_page_index + 1, len(self.current_song.pages)
                )
                yield PageInfo(
                    self.current_page_index + 1,
                    len(self.current_song.pages),
                )
                yield ActionButton("  ", "screen.next_page", classes="p-l-1 m-0")
        yield MainMenu(
            title=self.songbook.name,
            songs=self.songs,
            songbooks=self.songbooks,
            settings=self.settings,
            id="menu",
            classes="hidden",
        ).data_bind(disabled=SheetViewer.menu_shown)

    def auto_paginate(self) -> None:
        """Auto paginate the songs."""
        screen_height = self.app.size.height - 2
        for song in self.songs.values():
            if song.auto_paginate:
                lines = song.raw_pages[0].content.split("\n")
                pages = []
                for i in range(0, len(lines), screen_height):
                    page_content = "\n".join(lines[i : i + screen_height])
                    pages.append(
                        PageDTO(
                            content=page_content, file_type=song.raw_pages[0].file_type
                        )
                    )
                song.pages = pages

    def action_toggle_menu(self) -> None:
        self.menu_shown = not self.menu_shown
        menu = self.query_one(MainMenu)
        if self.menu_shown:
            menu.remove_class("hidden")
        else:
            menu.add_class("hidden")

    def action_settings(self) -> None:
        def fallback(data: Settings) -> None:
            self.settings = data
            self.notify(ok(" Settings saved."))

        self.app.push_screen(SettingsScreen(self.settings, self.songbooks), fallback)

    def action_show_songbook_overview(self) -> None:
        def fallback(data: tuple[int, SongbookDTO] | int) -> None:
            if isinstance(data, tuple):
                current_song_index, songbook = data
                self.current_song_index = current_song_index
                self.songbook = dataclasses.replace(songbook)
                self.notify(ok(f" Songbook {self.songbook.name} saved."))
            else:
                # only current song index got returned
                self.current_song_index = data

            self.current_page_index = 0

        self.app.push_screen(
            SongbookOverviewModal(self.songs, self.songbook, self.current_song_index),
            fallback,
        )

    def action_prev_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (
            self.current_song_index + self.songbook.size - 1
        ) % self.songbook.size

    def action_next_song(self) -> None:
        self.current_page_index = 0
        self.current_song_index = (self.current_song_index + 1) % self.songbook.size

    def action_prev_page(self) -> None:
        if self.current_page_index > 0:
            self.current_page_index -= 1
        else:
            self.action_prev_song()
            self.current_page_index = len(self.current_song.pages) - 1

    def action_next_page(self) -> None:
        if self.current_page_index < len(self.current_song.pages) - 1:
            self.current_page_index += 1
        else:
            self.action_next_song()

    async def action_refresh_sheet_viewer(self) -> None:
        self.auto_paginate()
        if self.current_page_index != 0:
            self.current_page_index = 0
        else:
            if self.current_page.file_type == FileType.TEXT:
                self.query_one(Label).update(
                    sheet_parser.markup(self.current_page.content)
                )
            else:
                self.query_one("#stc_md", Static).update(
                    Markdown(markup=self.current_page.content)
                )
