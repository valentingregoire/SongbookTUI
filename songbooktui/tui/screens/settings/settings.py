from dataclasses import asdict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Pretty, Input, Collapsible, Checkbox

from backend import service
from backend.model import Settings
from tui.widgets.form import Form
from tui.widgets.widget_factory import WidgetFactory


class SettingsScreen(Screen):
    CSS_PATH = "settings.tcss"

    settings: Settings
    settings_original: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = Settings(**asdict(settings))
        self.settings_original = Settings(**asdict(settings))
        super().__init__()

    def compose(self) -> ComposeResult:
        with Form(asdict(self.settings)):
            default_songbook_input = Input(
                placeholder="Default songbook",
                name="default_songbook",
                value=self.settings.default_songbook,
            )
            default_songbook_input.border_title = "Default songbook"
            yield default_songbook_input
            yield Checkbox("Some check as I said", name="some_check")
            yield WidgetFactory.actions_bar_form()

        with Collapsible(title="settings.json", collapsed=False):
            yield Pretty(asdict(self.settings))

    def action_ok(self) -> None:
        self.dismiss(self.settings)

    def action_cancel(self) -> None:
        self.settings = self.settings_original
        self.app.pop_screen()
        # self.dismiss(self.settings_original)

    def on_form_changed(self, event: Form.Changed) -> None:
        if hasattr(self.settings, event.name):
            setattr(self.settings, event.name, event.value)
            self.query_one(Pretty).update(asdict(self.settings))

    async def on_form_submit(self, event: Form.Submit) -> None:
        self.settings = Settings(**event.data)
        await service.save_settings(self.settings)
        self.dismiss(self.settings)
