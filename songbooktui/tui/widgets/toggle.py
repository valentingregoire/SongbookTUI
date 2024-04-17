from textual.app import RenderResult
from textual.events import Click
from textual.reactive import reactive
from textual.widget import Widget


class Toggle(Widget):
    DEFAULT_CSS = """
        Toggle {
            color: $primary;
            width: auto;
            padding: 0 1;
        }

        Toggle:hover {
            color: $primary-lighten-1;
        }

        Toggle.on {
            color: $primary-lighten-3;
        }

        Toggle.on:hover {
            color: $primary-lighten-3;
        }
    """

    action: str
    value: reactive[bool] = reactive(False, recompose=True)

    def __init__(
        self,
        action: str,
        value: bool = False,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.action = action
        self.value = value

    def render(self) -> RenderResult:
        # TODO: PUT IN custom action toggle
        if not self.value:
            self.remove_class("on")
            return "██░░"
        else:
            self.add_class("on")
            return "▓▓██"

    async def on_click(self, event: Click):
        event.stop()
        self.value = not self.value
        self.refresh()
        await self.run_action(self.action)
