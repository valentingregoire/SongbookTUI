from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, ContentSwitcher, Label, Markdown, Header, Footer


class ViewerApp(App):
    def on_mount(self) -> None:
        self.push_screen(ViewerScreen())

    def action_next_song(self) -> None:
        self.screen.action_next_song()


class ViewerScreen(Screen):
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("n", "next_song", "Next Song"),
    ]

    current_song_index: reactive[int] = reactive(0, recompose=True)

    def action_next_song(self) -> None:
        self.current_song_index += 1

    def compose(self) -> ComposeResult:
        # with VerticalScroll():
        with ContentSwitcher(initial="viewer_txt"):
            yield Label(str(self.current_song_index), id="viewer_txt")
            yield Markdown(
                "some markdown",
                id="viewer_md",
            )

        # yield Static("[@click=next_song]ns[/]", id="link_next_song", classes="link")
        yield Static("Go to [@click=next_song]Next Song[/] please!", id="link_next_song", classes="link")
        yield Header()
        yield Footer()


class TestApp(App):
    some_var = reactive("some text")

    def compose(self) -> ComposeResult:
        yield Static(self.some_var)
        yield Static("[@click=set_background('orange')]Orange[/]")

    def action_set_background(self, color: str) -> None:
        self.some_var += "hallo"
        self.screen.styles.background = color


if __name__ == "__main__":
    app = ViewerApp()
    app.run()
