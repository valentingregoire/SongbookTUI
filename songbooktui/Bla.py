from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header

class ScreenTitleApp(App[None]):

    BINDINGS = [
        ("space", "title"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

    def on_mount(self) -> None:
        self.screen.title = "Here is the title"

    def action_title(self) -> None:
        self.screen.title = reactive("Here is the title")

if __name__ == "__main__":
    ScreenTitleApp().run()