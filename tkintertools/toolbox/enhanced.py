"""Enhanced versions of some tkinter classes and functions"""

__all__ = [
    "PhotoImage",
]

import functools
import tkinter

try:
    from PIL import ImageTk
except ImportError:
    ImageTk = None


if not ImageTk:

    class PhotoImage(tkinter.PhotoImage):
        """Enhanced version of `tkinter.PhotoImage`"""

        @functools.cached_property
        def _data(self) -> list[list[str]]:
            """Return image data in the form of a string"""
            # self.tk.call(self, "data", "-format", "png -alpha 0")
            # XXX: Add alpha channel
            return [line.split() for line in self.tk.call(self, "data")]

        @functools.cached_property
        def _transparency_data(self) -> list[list[bool]]:
            """Return transparency data of the image"""
            return [[self.transparency_get(x, y)
                    for x in range(self.width())]
                    for y in range(self.height())]

        def scale(self, x: float, y: float) -> "PhotoImage":
            """Scale the PhotoImage"""
            width = round(x*self.width())
            height = round(y*self.height())
            return self.resize(width, height)

        def resize(self, width: int, height: int) -> "PhotoImage":
            """Resize the PhotoImage"""
            x = width / self.width()
            y = height / self.height()
            new_image = PhotoImage(width=width, height=height)
            new_image.put([[self._data[int(j/y)][int(i/x)]
                            for i in range(width)] for j in range(height)])

            for i in range(width):
                for j in range(height):
                    if self._transparency_data[int(j/y)][int(i/x)]:
                        new_image.transparency_set(i, j, True)

            return new_image

else:

    class PhotoImage(ImageTk.PhotoImage, tkinter.PhotoImage):
        """Pillow version of `tkinter.PhotoImage`"""

        def scale(self, x: float, y: float) -> "PhotoImage":
            """Scale the PhotoImage"""
            width = round(x*self.width())
            height = round(y*self.height())
            return self.resize(width, height)

        def resize(self, width: int, height: int) -> "PhotoImage":
            """Resize the PhotoImage"""
            return PhotoImage(ImageTk.getimage(self).resize((width, height)))
