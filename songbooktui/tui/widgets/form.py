from textual.containers import Container
from textual.message import Message
from textual.widgets import RadioSet, Checkbox, Input, Select


class Form(Container):
    DEFAULT_CSS = """
        Form {
        }
    """

    data: dict[str, any]

    def __init__(self, data: dict[str, any]):
        self.data = data
        super().__init__()

    class Changed(Message):
        name: str
        value: any
        message: Message

        def __init__(self, name: str, value: any, message: Message):
            super().__init__()
            self.name = name
            self.value = value
            self.message = message

    class PreSubmit(Message):
        pass

    class Submit(Message):
        data: dict[str, any]

        def __init__(self, data: dict[str, any] = None):
            self.data = data
            super().__init__()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        self.handle_events(event.checkbox.name, event.checkbox.value, event)

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.handle_events(event.radio_set.name, event.radio_set.pressed_index, event)

    def on_input_changed(self, event: Input.Changed) -> None:
        self.handle_events(event.input.name, event.input.value, event)

    def on_select_changed(self, event: Select.Changed) -> None:
        self.handle_events(event.select.name, event.select.value, event)

    def on_form_pre_submit(self, event: PreSubmit) -> None:
        self.post_message(self.Submit(self.data))

    def handle_events(self, name: str, value: any, message: Message) -> None:
        self.data[name] = value
        self.post_message(self.Changed(name, value, message))
