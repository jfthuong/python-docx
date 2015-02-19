# encoding: utf-8

"""
DrawingML objects related to color, ColorFormat being the most prominent.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.dml import MSO_COLOR_TYPE
from ..oxml.simpletypes import ST_HexColorAuto
from ..shared import ElementProxy


class ColorFormat(ElementProxy):
    """
    Provides access to color settings such as RGB color, theme color, and
    luminance adjustments.
    """

    __slots__ = ()

    def __init__(self, rPr_parent):
        super(ColorFormat, self).__init__(rPr_parent)

    @property
    def rgb(self):
        """
        An |RGBColor| value or |None| if no RGB color is specified.

        When :attr:`type` is `MSO_COLOR_TYPE.RGB`, the value of this property
        will always be an |RGBColor| value. It may also be an |RGBColor|
        value if :attr:`type` is `MSO_COLOR_TYPE.THEME`, as Word writes the
        current value of a theme color when one is assigned. In that case,
        the RGB value should be interpreted as no more than a good guess
        however, as the theme color takes precedence at rendering time. Its
        value is |None| whenever :attr:`type` is either |None| or
        `MSO_COLOR_TYPE.AUTO`.

        Assigning an |RGBColor| value causes :attr:`type` to become
        `MSO_COLOR_TYPE.RGB` and any theme color is removed. Assigning |None|
        causes any color to be removed such that the effective color is
        inherited from the style hierarchy.
        """
        color = self._color
        if color is None:
            return None
        if color.val == ST_HexColorAuto.AUTO:
            return None
        return color.val

    @property
    def type(self):
        """
        Read-only. A member of :ref:`MsoColorType`, one of RGB, THEME, or
        AUTO, corresponding to the way this color is defined. Its value is
        |None| if no color is applied at this level, which causes the
        effective color to be inherited from the style hierarchy.
        """
        color = self._color
        if color is None:
            return None
        if color.themeColor is not None:
            return MSO_COLOR_TYPE.THEME
        if color.val == ST_HexColorAuto.AUTO:
            return MSO_COLOR_TYPE.AUTO
        return MSO_COLOR_TYPE.RGB

    @property
    def _color(self):
        """
        Return `w:rPr/w:color` or |None| if not present. Helper to factor out
        repetitive element access.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.color