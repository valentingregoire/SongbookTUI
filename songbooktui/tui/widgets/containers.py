from textual.containers import Horizontal


class TopBar(Horizontal):
    DEFAULT_CSS = """
    TopBar {
        # border: round magenta;
        align: center top;
        height: 1;
        dock: top;
        # opacity: 1;
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
        # layout: horizontal;
        align: center middle;
        content-align: center middle;
        text-align: center;
        # background: yellow;
        # width: auto;
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
