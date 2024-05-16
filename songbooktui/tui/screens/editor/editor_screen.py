from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Select, TextArea

from backend import service
from backend.dto import SongDTO
from tui.utils import ok
from tui.widgets.widget_factory import WidgetFactory


class EditorScreen(Screen):
    """The editor screen for the Songbook TUI."""

    CSS_PATH = "editor_screen.tcss"

    song: SongDTO

    def __init__(self, song: SongDTO) -> None:
        self.song = song
        super().__init__()

    def compose(self) -> ComposeResult:
        if len(self.song.raw_pages) > 1:
            yield Select(
                (
                    (f"{i + 1}.{page.file_type}", i)
                    for i, page in enumerate(self.song.raw_pages)
                ),
                allow_blank=False,
            )
        if self.song.pages[0].file_type == "txt":
            yield TextArea(id="editor_txt", text=self.song.raw_pages[0].content)
        else:
            yield TextArea.code_editor(
                id="editor_md", text=self.song.raw_pages[0].content, language="markdown"
            )
        # yield TextArea(text=self.song.raw_pages[0].content)
        yield WidgetFactory.actions_bar(
            [
                WidgetFactory.btn_save(),
                WidgetFactory.btn_ok(),
            ]
        )

    async def on_select_changed(self, event: Select.Changed) -> None:
        """Handle the select changed event."""
        if self.song.raw_pages[event.value].file_type == "txt":
            editor = self.query_one("#editor_txt", TextArea)
        else:
            editor = self.query_one("#editor_md", TextArea)
        editor.text = self.song.raw_pages[event.value].content

    async def action_save(self) -> None:
        """Save the song."""
        current_page_index = (
            self.query_one(Select).value if len(self.song.raw_pages) > 1 else 0
        )
        editor = self.query_one(TextArea)
        current_page = self.song.raw_pages[current_page_index]
        current_page.content = editor.text
        await service.save_page(current_page, self.song.id, current_page_index + 1)
        self.notify(
            ok(f" {self.song.title} page {current_page_index + 1} saved successfully.")
        )

    async def action_ok(self) -> None:
        """Close the editor screen."""
        self.dismiss(self.song)
