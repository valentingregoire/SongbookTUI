from textual.reactive import reactive
from textual.widget import Widget


class TextViewer(Widget):
    """A widget for displaying text based sheets."""

    content: reactive[str]

    def __init__(self, content: str) -> None:
        self.content = content
        super().__init__()

    def render(self) -> str:
        return self.content

