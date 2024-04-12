from textual.reactive import reactive
from textual.widget import Widget


class SongInfo(Widget):
    DEFAULT_CSS = """
    SongInfo {
        content-align: right middle;
        # margin: 0 1;
        width: auto;
        text-style: bold;
    }
    """
    song_number: reactive[int] = reactive(1)
    total_songs: reactive[int] = reactive(1)

    def __init__(
        self, song_number: int = 1, total_songs: int = 1, id: str | None = None
    ) -> None:
        super().__init__(id=id)
        self.song_number = song_number
        self.total_songs = total_songs

    def render(self) -> str:
        return f"#{self.song_number}/{self.total_songs}"
