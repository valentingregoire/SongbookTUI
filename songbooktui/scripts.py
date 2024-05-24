import argparse

from tui.app import SongbookApp
from tui.utils import VERSION


def main() -> None:
    parser = argparse.ArgumentParser(description="📒 Songbook")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{VERSION}",
        help="Print the version and exit.",
    )
    parser.parse_args()
    app = SongbookApp()
    app.run()
