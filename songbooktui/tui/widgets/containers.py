from textual.app import RenderResult
from textual.containers import Horizontal
from textual.widget import Widget


class Spacer(Widget):
    DEFAULT_CSS = """
    Spacer {
        width: auto;
        background: red;
    }
    """

    height: int

    def __init__(self, height: int = 1) -> None:
        super().__init__()
        self.height = height

    def on_mount(self) -> None:
        self.styles.height = self.height

    def render(self) -> RenderResult:
        return "";


class TopBar(Horizontal):
    DEFAULT_CSS = """
    TopBar {
        # border: round magenta;
        align: center top;
        height: 1;
        width: auto;
        dock: top;
        # opacity: 1;
        background: red;
    }
    """


class BottomBar(Horizontal):
    DEFAULT_CSS = """
    BottomBar {
        # border: round yellow;
        content-align: center bottom;
        height: 1;
        dock: bottom;
        # opacity: 0.5;
        # background: red;
    }
    """


class HorizontalFloat(Horizontal):
    DEFAULT_CSS = """
    HorizontalFloat {
        height: 1;
        width: auto;
        align: center middle;
        content-align: center middle;
        text-align: center;
        background: red 0%;
    }
    """
    # pass


class LeftFloat(HorizontalFloat):
    DEFAULT_CSS = """
    LeftFloat {
        align: left middle;
        content-align: left middle;
        # background: red;
        width: 30%;
    }
    """


class CenterFloat(HorizontalFloat):
    DEFAULT_CSS = """
    MiddleFloat {
        align: center middle;
        content-align: center middle;
        text-align: center;
        # background: green;
        # width: auto;
    }
    """


class RightFloat(HorizontalFloat):
    DEFAULT_CSS = """
    RightFloat {
        align: right middle;
        content-align: right middle;
        # background: blue;
        width: 30%;
    }
    """
