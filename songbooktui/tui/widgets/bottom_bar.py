from textual.reactive import reactive
from textual.widget import Widget


class PageInfo(Widget):
    DEFAULT_CSS = """
    PageInfo {
        content-align: right middle;
        margin: 0 1;
        width: auto;
        text-style: bold;
    }
    """
    page_number: reactive[int] = reactive(1)
    total_pages: reactive[int] = reactive(1)

    def __init__(
            self, page_number: int = 1, total_pages: int = 1, id: str | None = None
    ) -> None:
        super().__init__(id=id)
        self.page_number = page_number
        self.total_pages = total_pages

    def render(self) -> str:
        return f"󰈙 {self.page_number}/{self.total_pages}"
