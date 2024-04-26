from rich.style import Style
from textual.app import App, ComposeResult
from textual.widgets import Static


class BorkedApp(App):
    """The main application class for the Songbook TUI."""

    text = "Hello, world!"
    style = Style(bgcolor="#333333", bold=True)
    text_styled = style.render(text)

    CSS_PATH = "app.tcss"
    DEFAULT_CSS = """
        Static {
            width: auto;
            border: round green;
        }
    """
    BINDINGS = [("q", "exit", "Quit")]

    def compose(self) -> ComposeResult:
        """Compose the main application."""
        yield Static(self.text)
        yield Static(self.text_styled, markup=False)


if __name__ == "__main__":
    app = BorkedApp()
    app.run()
