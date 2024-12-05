"""
@package mapwin.graphics

@brief Map display canvas - buffered window.

Classes:
 - graphics::GraphicsSet
 - graphics::GraphicsSetItem

(C) 2006-2013 by the GRASS Development Team

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author Stepan Turek <stepan.turek seznam.cz> (handlers support, GraphicsSet)
"""

from copy import copy

import wx

from gui_core.wrap import NewId


class GraphicsSet:
    def __init__(
        self,
        parentMapWin,
        graphicsType,
        pdc,
        setStatusFunc=None,
        drawFunc=None,
        mapCoords=True,
    ):
        """Class, which contains instances of GraphicsSetItem and
        draws them For description of parameters look at method
        RegisterGraphicsToDraw in BufferedWindow class.
        """
        self.pens = {
            "default": wx.Pen(colour=wx.BLACK, width=2, style=wx.SOLID),
            "selected": wx.Pen(colour=wx.GREEN, width=2, style=wx.SOLID),
            "unused": wx.Pen(colour=wx.LIGHT_GREY, width=2, style=wx.SOLID),
            "highest": wx.Pen(colour=wx.RED, width=2, style=wx.SOLID),
        }
        self.brushes = {"default": wx.TRANSPARENT_BRUSH}

        # list contains instances of GraphicsSetItem
        self.itemsList = []

        self.properties = {}
        self.graphicsType = graphics