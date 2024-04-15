CHECKMARK = " "
# _CROSSMARK = " "
CROSSMARK = " "
PENSIL = " "

DEFAULT_BINDINGS = [
    ("c", "pop_screen", "Cancel"),
    ("o", "ok", "Ok"),
]

def ok(text: str = "OK") -> str:
    return f"{CHECKMARK}{text}"


def cancel(text: str = "Cancel") -> str:
    return f"{CROSSMARK}{text}"