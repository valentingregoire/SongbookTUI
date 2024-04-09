_CHECKMARK = " "
# _CROSSMARK = " "
_CROSSMARK = " "


def check(text: str = "OK") -> str:
    return f"{_CHECKMARK}{text}"


def cancel(text: str = "Cancel") -> str:
    return f"{_CROSSMARK}{text}"