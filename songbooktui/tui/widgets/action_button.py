from textual.app import RenderResult
from textual.events import Click
from textual.reactive import reactive
from textual.widget import Widget


class ActionButton(Widget):
    DEFAULT_CSS = """
    ActionButton {
        content-align: center top;
        width: auto;
        padding: 0 1;
        margin: 0 1;
        height: 1;
    }
    
    ActionButton:hover {
        background: $foreground 10%;
    }
    """

    text: reactive[str] = reactive("󱓻 ")
    action: str

    def __init__(
        self,
        text: str,
        action: str,
        id: str | None = None,
        classes: str | None = None,
        *args,
    ) -> None:
        super().__init__(id=id, classes=classes, *args)
        self.text = text
        self.action = action

    def render(self) -> RenderResult:
        return self.text

    async def on_click(self, event: Click) -> None:
        event.stop()
        await self.run_action(self.action)
