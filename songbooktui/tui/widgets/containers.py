from textual.containers import Horizontal


class TopBar(Horizontal):
    DEFAULT_CSS = """
    TopBar {
        layout: horizontal;
        height: 1;
        dock: top;
        opacity: 0.5;
    }
    """


class BottomBar(Horizontal):
    DEFAULT_CSS = """
    TopBar {
        layout: horizontal;
        height: 1;
        dock: bottom;
        opacity: 0.5;
        background: red;
    }
    """


class LeftFloat(Horizontal):
    DEFAULT_CSS = """
    LeftFloat {
        align: left middle;
        content-align: left middle;
        # background: red;
        # width: 30%;
    }
    """


class CenterFloat(Horizontal):
    DEFAULT_CSS = """
    MiddleFloat {
        align: center middle;
        content-align: center middle;
        text-align: center;
        # background: green;
    }
    """


class RightFloat(Horizontal):
    DEFAULT_CSS = """
    RightFloat {
        align: right middle;
        content-align: right middle;
        # background: blue;
        # width: 50%;
    }
    """
