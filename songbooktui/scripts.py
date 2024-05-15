from .tui.app import SongbookApp


def main() -> None:
    app = SongbookApp()
    app.run()
