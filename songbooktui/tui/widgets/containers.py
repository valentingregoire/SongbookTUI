from textual.app import RenderResult
from textual.containers import Horizontal
from textual.widget import Widget


class Spacer(Widget):
    DEFAULT_CSS = """
    Spacer {
        width: auto;
    }
    """

    height: int

    def __init__(self, height: int = 1) -> None:
        super().__init__()
        self.height = height

    def on_mount(self) -> None:
        self.styles.height = self.height

    def render(self) -> RenderResult:
        return ""


class ActionsBar(Horizontal):
    DEFAULT_CSS = """
    ActionsBar {
        align: right middle;
        content-align: right middle;
        height: 1;
        width: 100%;
        margin-top: 1;
    }
    """


class TopBar(Horizontal):
    DEFAULT_CSS = """
    TopBar {
        align: center top;
        height: 1;
        width: 100%;
        dock: top;
    }
    """


class BottomBar(Horizontal):
    DEFAULT_CSS = """
    BottomBar {
        align: center bottom;
        content-align: center bottom;
        height: 1;
        width: 100%;
        dock: left;  # FIXME: why doesn't this work with dock: bottom??
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
        width: auto;
        # width: 30%;
        height: 1;
        # width: 1fr;
    }
    """


class CenterFloat(HorizontalFloat):
    DEFAULT_CSS = """
    CenterFloat {
        align: center middle;
        content-align: center middle;
        text-align: center;
        width: auto;
        height: 1;
    }
    """


class RightFloat(HorizontalFloat):
    DEFAULT_CSS = """
    RightFloat {
        align: right middle;
        content-align: right middle;
        # background: blue;
        width: 1fr;
        # width: auto;
        height: 1;
    }
    """
