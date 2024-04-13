_CHECKMARK = " "
# _CROSSMARK = " "
_CROSSMARK = " "

DEFAULT_BINDINGS = [
    ("c", "pop_screen", "Cancel"),
    ("o", "ok", "Ok"),
]

def ok(text: str = "OK") -> str:
    return f"{_CHECKMARK}{text}"


def cancel(text: str = "Cancel") -> str:
    return f"{_CROSSMARK}{text}"