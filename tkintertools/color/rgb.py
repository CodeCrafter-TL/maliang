"""Support for RGB"""

__all__ = [
    "contrast",
    "convert",
    "blend",
    "gradient",
    "str_to_rgb",
    "str2rgb",
    "rgb_to_str",
    "rgb2str",
]

import statistics
import typing

from ..animation import controllers
from . import colormap


RGB = tuple[int, int, int]
"""
R: Red, 0 ~ 255
G: Green, 0 ~ 255
B: Blue, 0 ~ 255
"""

MAX = 255, 255, 255
"""The maximum value of the RGB code"""


def contrast(
    rgb: RGB,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> RGB:
    """Get a contrasting color of a color

    * `rgb`: a tuple, RGB codes
    * `channels`: three color channels
    """
    return tuple(map(lambda x: x[0] * (x[1]-x[2]), zip(channels, MAX, rgb)))


def convert(
    first: RGB,
    second: RGB,
    rate: float,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> RGB:
    """Convert one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `rate`: conversion rate
    * `channels`: three color channels
    """
    return tuple(first[i] + round((second[i]-first[i])*rate*v)
                 for i, v in enumerate(channels))


def blend(
    colors: list[RGB],
    *,
    weights: list[tuple] | None = None
) -> RGB:
    """Mix colors by weight

    * `colors`: color list
    * `weights`: weight list
    """
    colors = zip(*colors)

    if weights is None:  # Same weights
        return tuple(map(lambda x: round(statistics.mean(x)), colors))

    _total = sum(weights)
    weights = tuple(map(lambda x: x/_total, weights))  # Different weights

    return tuple(round(sum(map(lambda x: x[0]*x[1], zip(c, weights))))
                 for c in colors)


def gradient(
    first: RGB,
    second: RGB,
    count: int,
    rate: float = 1,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
    contoller: typing.Callable[[float], float] = controllers.flat,
) -> list[RGB]:
    """Get a list of color gradients from one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `count`: number of gradients
    * `rate`: conversion rate
    * `channels`: three color channels
    * `controller`: control function
    """
    rgb_list: list[RGB] = []
    delta = tuple(rate * (j-i) * k for i, j, k in zip(first, second, channels))

    for x in (contoller(i/count) for i in range(count)):
        rgb_list.append(tuple(c + round(x*r) for c, r in zip(first, delta)))

    return rgb_list


def str_to_rgb(color: str) -> RGB:
    """Convert color strings to RGB codes"""
    if color.startswith("#"):  # HEX
        hex, b = divmod(int(color[1:], 16), 256)
        r, g = divmod(hex, 256)
        return r, g, b

    return colormap.name_to_rgb(color)


str2rgb = str_to_rgb  # Alias


def rgb_to_str(rgb: RGB) -> str:
    """Convert RGB codes to color strings"""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


rgb2str = rgb_to_str  # Alias


def _str_to_rgba(color: str, *, reference: str) -> RGB:
    """Experimental: Convert color strings(RGBA) to RGB codes"""
    hex, a = divmod(int(color[1:], 16), 256)
    hex, b = divmod(hex, 256)
    r, g = divmod(hex, 256)
    refer_rgb = str_to_rgb(reference)
    return convert((r, g, b), refer_rgb, 1 - a/255)


_str2rgba = _str_to_rgba  # Alias
