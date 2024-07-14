from dataclasses import asdict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Pretty, Collapsible, Select, Static, Checkbox

from backend import service
from backend.dto import SongbookDTO
from backend.model import Settings
from tui.widgets.form import Form
from tui.widgets.widget_factory import WidgetFactory


class SettingsScreen(Screen):
    CSS_PATH = "settings.tcss"

    settings: Settings
    settings_original: Settings
    songbooks: dict[int, SongbookDTO]

    def __init__(self, settings: Settings, songbooks: dict[int, SongbookDTO]) -> None:
        self.settings = Settings(**asdict(settings))
        self.settings_original = Settings(**asdict(settings))
        self.songbooks = songbooks
        super().__init__()

    def compose(self) -> ComposeResult:
        with Form(asdict(self.settings)):
            yield Static("Default songbook")
            default_songbook_options = [(s.name, s.id) for s in self.songbooks.values()]
            default_songbook_select: Select[int] = Select(
                options=default_songbook_options,
                name="default_songbook",
                allow_blank=False,
                value=self.songbooks.get(self.settings.default_songbook).id,
            )
            default_songbook_select.border_title = "Default songbook"
            yield default_songbook_select
            yield Checkbox(
                "Hide navigation buttons",
                self.settings.hide_nav_buttons,
                name="hide_nav_buttons",
            )
            yield WidgetFactory.actions_bar_form()

        with Collapsible(title="settings.json", collapsed=False):
            yield Pretty(asdict(self.settings))

    def action_ok(self) -> None:
        self.dismiss(self.settings)

    def action_cancel(self) -> None:
        self.settings = self.settings_original
        self.app.pop_screen()

    def on_form_changed(self, event: Form.Changed) -> None:
        if hasattr(self.settings, event.name):
            setattr(self.settings, event.name, event.value)
            self.query_one(Pretty).update(asdict(self.settings))

    async def on_form_submit(self, event: Form.Submit) -> None:
        self.settings = Settings(**event.data)
        await service.save_settings(self.settings)
        self.dismiss(self.settings)
