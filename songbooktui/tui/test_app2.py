from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Button, Input, Static


class DisableApp(App):
    edit_mode: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        yield Button("Edit", id="btn_edit")
        with Vertical(id="container").data_bind(disabled=DisableApp.edit_mode):
            yield Input(placeholder="Name")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.edit_mode = not self.edit_mode
        self.log(self.edit_mode)


class FizzBuzz(Static):
    def on_mount(self) -> None:
        table = Table("Number", "Fizz?", "Buzz?")
        for n in range(1, 16):
            fizz = not n % 3
            buzz = not n % 5
            table.add_row(
                str(n),
                "fizz" if fizz else "",
                "buzz" if buzz else "",
            )
        self.update(table)


class FizzBuzzApp(App):
    DEFAULT_CSS = """
    Screen {
        align: center middle;
    }

    FizzBuzz {
        width: auto;
        height: auto;
        background: $primary;
        color: $text;
    }
    """

    def compose(self) -> ComposeResult:
        yield FizzBuzz()


if __name__ == "__main__":
    # app = FizzBuzzApp()
    app = DisableApp()
    app.run()

# class ViewerApp(App):
#     def on_mount(self) -> None:
#         self.push_screen(ViewerScreen())

#     def action_next_song(self) -> None:
#         self.screen.action_next_song()


# class ViewerScreen(Screen):
#     BINDINGS = [
#         ("q", "app.quit", "Quit"),
#         ("n", "next_song", "Next Song"),
#     ]

#     current_song_index: reactive[int] = reactive(0, recompose=True)

#     def action_next_song(self) -> None:
#         self.current_song_index += 1

#     def compose(self) -> ComposeResult:
#         # with VerticalScroll():
#         with ContentSwitcher(initial="viewer_txt"):
#             yield Label(str(self.current_song_index), id="viewer_txt")
#             yield Markdown(
#                 "some markdown",
#                 id="viewer_md",
#             )

#         # yield Static("[@click=next_song]ns[/]", id="link_next_song", classes="link")
#         yield Static(
#             "Go to [@click=next_song]Next Song[/] please!",
#             id="link_next_song",
#             classes="link",
#         )
#         yield Header()
#         yield Footer()


# class TestApp(App):
#     some_var = reactive("some text")

#     def compose(self) -> ComposeResult:
#         yield Static(self.some_var)
#         yield Static("[@click=set_background('orange')]Orange[/]")

#     def action_set_background(self, color: str) -> None:
#         self.some_var += "hallo"
#         self.screen.styles.background = color


# if __name__ == "__main__":
#     app = ViewerApp()
#     app.run()
