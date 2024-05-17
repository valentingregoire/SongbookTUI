import re


# Horizontal whitespace (\h)
# _H = r"[^\S\r\n]"
_H = r"[\t |┃]"
CHORD_REGEX = (
    r"[A-G](?:b|#)?(?:maj|min|m|M|\+|-|dim|aug)?\d*(?:sus)?(?:2|4)?(?:\/[A-G](?:b|#)?)?"
)
CHORD_LINE_REGEX = rf"^(?:{_H}*{CHORD_REGEX}{_H}*)+(?:x\d?\.*)?$"


def markup(sheet: str) -> str:
    """Mark chords and headers in the sheet music with special characters."""
    sheet = _mark_chords(sheet)
    sheet = _mark_h2(sheet)
    sheet = _mark_h1(sheet)
    return sheet


def _mark_chords(sheet: str) -> str:
    """Mark chords in the sheet music with special characters."""
    # Find all lines that contain only chords.
    matches = re.findall(CHORD_LINE_REGEX, sheet, re.MULTILINE)
    for match in matches:
        # Replace every chord with the styled chord and then replace the entire line.
        match_replaced = re.sub(CHORD_REGEX, lambda x: _style_chord(x.group()), match)
        sheet = re.sub(match.replace("|", "\\|"), match_replaced, sheet, count=1)
    return sheet


def _mark_h1(sheet: str) -> str:
    """Mark headers in the sheet music with special characters."""
    # Find all lines that contain only chords.
    return re.sub(
        r"^\[([\w -]+)]$",
        lambda x: _style_h1(x.group(1)),
        sheet,
        flags=re.MULTILINE,
    )


def _mark_h2(sheet: str) -> str:
    """Mark headers in the sheet music with special characters."""
    # Find all lines that contain only chords.
    return re.sub(
        r"^\[\[([\w -]+)]]$",
        lambda x: _style_h2(x.group(1)),
        sheet,
        flags=re.MULTILINE,
    )


def _style_chord(chord: str) -> str:
    """Style a chord with a rich style."""
    # style = Style(bgcolor="#333333", bold=True)
    # rendered_chord = style.render(chord)
    rendered_chord = f"[b white on #333333]{chord}[/]"
    return rendered_chord


def _style_h1(title: str) -> str:
    """Style a title with a rich style."""
    # style = Style(color="deep_sky_blue1", bold=True)
    # rendered_title = style.render(title)
    rendered_title = f"[b deep_sky_blue1]{title}[/]"
    return rendered_title


def _style_h2(title: str) -> str:
    """Style a title with a rich style."""
    # style = Style(color="orange1", italic=True)
    # rendered_title = style.render(title)
    rendered_title = f"[b i orange1]{title}[/]"
    return rendered_title
