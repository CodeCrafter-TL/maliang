"""Internal Module: Some utility functions"""


import typing

try:
    import winreg
except ImportError:
    winreg = None


def is_dark() -> bool | None:
    """Determine whether the operating system is a dark theme"""
    if winreg is None:
        return None
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
        return not winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
    except FileNotFoundError:
        return None


def get_control_lst(
    controller: tuple[typing.Callable[[float], float], float, float],
    length: int,
) -> list[float]:
    """Get a list of floating-point numbers generated by a control function"""
    delta = controller[2] - controller[1]
    lst = [controller[0](controller[1] + i/length*delta)
           for i in range(1, length+1)]
    if (maximum := max(lst)) == 0:
        return [controller[0](controller[1])] * length
    return [value/maximum for value in lst]


def info(value: str) -> None:
    """Output a piece of information"""
    print(f"\033[36mInfo: {value}\033[0m")


def warning(value: str) -> None:
    """Output a warning"""
    print(f"\033[33mWarning: {value}\033[0m")


def error(value: str) -> None:
    """Output an error"""
    print(f"\033[31mError: {value}\033[0m")
