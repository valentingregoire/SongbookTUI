from textual.reactive import reactive
from textual.widget import Widget


class InlineVerticalProgressBar(Widget):
    _1_8 = "▁"
    _2_8 = "▂"
    _3_8 = "▃"
    _4_8 = "▄"
    _5_8 = "▅"
    _6_8 = "▆"
    _7_8 = "▇"
    _8_8 = "█"

    DEFAULT_CSS = """
    InlineVerticalProgressBar {
        content-align: center middle;
        width: auto;
    }
    """

    progress: reactive[float] = reactive(0)
    total: reactive[float] = reactive(1)

    def __init__(
        self, progress: float = 0, total: float = 1, id: str | None = None
    ) -> None:
        super().__init__(id=id)
        self.progress = progress
        self.total = total

    def render(self) -> None:
        progress = self.progress / self.total
        progress_str = " "
        if progress == 1:
            progress_str = self._8_8
        elif progress >= 7 / 8:
            progress_str = self._7_8
        elif progress >= 6 / 8:
            progress_str = self._6_8
        elif progress >= 5 / 8:
            progress_str = self._5_8
        elif progress >= 4 / 8:
            progress_str = self._4_8
        elif progress >= 3 / 8:
            progress_str = self._3_8
        elif progress >= 2 / 8:
            progress_str = self._2_8
        elif progress >= 1 / 8:
            progress_str = self._1_8
        return progress_str * 2

    def update(self, progress: float) -> None:
        self.progress = progress
        # self.refresh()
