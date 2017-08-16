"""
The UI module
===============

This module handles everything about the ui : buttons, titles, menus...

Widgets are organizes in layouts.

"""

import pygame
from pygame.locals import *

from bubble_platform.pos_in_rect import pos_in_rect

WIDGET_MARGIN = 10
WIDGET_PADDING = 10


class Button():
    """
    A button in the ui.
    """

    def __init__(self, rc_manager, **kwargs):
        """
        The __init__ method.

        :param rc_manager: The resources manager of the application.
        :param text: Some text to be displayed in the widget. (default = " ")
        :param font: The font which is to be used. (default = "default_font")
        :param color: The color of the text. (default = (0,0,0))
        :param background: Background color (default = None)
        :param border: color of the border (default = None)
        :param border_width: width of the border (default = 0)
        :param callback: A function to call when clicked. (default = lambda :
            None)
        :param min_width: A minimum width for the button. (default = 0)
        :param min_height:A minimum height for the button. (default = 0)

        :type rc_manager: ResourceManager
        :type text: str
        :type color: (int,int,int)
        :type font: str
        :type background: (int, int, int)
        :type border: (int, int, int)
        :type border_width: int
        :type callback: function
        :type min_width: int
        :type min_height: int
        """

        self.rc_manager = rc_manager
        self.text = kwargs.get("text", " ")
        self.font = kwargs.get("font", "default_font")
        self.color = kwargs.get("color", (0, 0, 0))
        self.background = kwargs.get("background", None)
        self.border = kwargs.get("border", None)
        self.border_width = kwargs.get("border_width", 0)
        self.callback = kwargs.get("callback", lambda : None)
        self.min_width = kwargs.get("min_width", 0)
        self.min_height = kwargs.get("min_height", 0)

        self.rect = (0, 0, 0, 0)
        self.hovered = False
        self.clicked = False

    def min_size(self):
        """
        Returns the minimum size the widget needs to be drawn.
        """
        w, h = self.rc_manager.get(self.font).size(self.text)
        return (max(self.min_width,w+2*WIDGET_PADDING), max(self.min_height,h+2*WIDGET_PADDING))

    def render_border(self, dst):
        if self.border and self.border_width > 0:
            pygame.draw.rect(dst, self.border, self.rect)

    def render_background(self, dst):
        x,y,w,h = self.rect
        if self.background:
            c = self.background
            if self.clicked and self.hovered:
                c = (
                    255 - c[0],
                    255 - c[1],
                    255 - c[2],
                )
            elif self.hovered:
                c = (
                    min((c[0]+10),255),
                    min((c[1]+10),255),
                    min((c[2]+10),255),
                )
            rect_bg = (
                x + self.border_width,
                y + self.border_width,
                w - 2*self.border_width,
                h - 2*self.border_width
            )
            pygame.draw.rect(dst, c, rect_bg)

    def render_font(self, dst):
        x,y,w,h = self.rect
        font = self.rc_manager.get(self.font)
        w_f, h_f = font.size(self.text)
        c = self.color
        if self.clicked and self.hovered:
            c = (
                255 - c[0],
                255 - c[1],
                255 - c[2],
            )
        dst.blit(
            font.render(self.text, True, c), 
            (
                x + (w - w_f) / 2,
                y + (h - h_f) / 2
            )
        )

    def on_render(self, dst, rect):
        """
        Render the widget on the given destination

        :param dst: The destination.
        :param rect: (x, y, width, height) of the widget.
        """
        self.rect = rect

        self.render_border(dst)
        self.render_background(dst)
        self.render_font(dst)

    def on_event(self, e):
        """
        Process the event.
        :param e: The event.
        """
        if e.type == MOUSEMOTION:
            self.hovered = pos_in_rect(e.pos, self.rect)
        elif e.type == MOUSEBUTTONDOWN:
            self.clicked = pos_in_rect(e.pos, self.rect)
        elif e.type == MOUSEBUTTONUP:
            self.clicked = False
            if pos_in_rect(e.pos, self.rect):
                self.callback()

class ImageButton(Button):
    """
    Same as Button except that it displays an image at the left of the text.
    """
    def __init__(self, *args, **kwargs):
        """
        The __init__ method.
        See the Button __init__ method for most of the arguments.

        :param image: The image which is to be displayed.
        """ 
        super(ImageButton, self).__init__(*args, **kwargs)
        self.image = kwargs['image']

    def min_size(self):
        w,h = super(ImageButton, self).min_size()
        w_i, h_i = self.rc_manager.get(self.image).get_size()

        return (w + w_i + WIDGET_PADDING, max(h + 2*WIDGET_PADDING, h_i))

    def render_font(self, dst):
        x,y,w,h = self.rect
        font = self.rc_manager.get(self.font)
        w_f, h_f = font.size(self.text)
        c = self.color
        if self.clicked and self.hovered:
            c = (
                255 - c[0],
                255 - c[1],
                255 - c[2],
            )
        dst.blit(
            font.render(self.text, True, c), 
            (
                x + WIDGET_PADDING + self.image_width,
                y + (h - h_f) / 2
            )
        )

    def on_render(self, *args, **kwargs):
        """
        Render the widget on the given destination

        See the Button doc.
        """
        image = self.rc_manager.get(self.image)
        self.image_width = image.get_width()
        super(ImageButton, self).on_render(*args, **kwargs)

        dst.blit(
            image,
            (
                x + WIDGET_PADDING,
                y + (h - image.get_height())/2
            )
        )
        

class VLayout():
    """
    A vertical layout.
    """

    def __init__(self):
        """
        The __init__ method.
        """
        self.widgets = []

    def size(self):
        """
        Returns the size of the layout.
        """
        w, h = zip(*map(lambda x: x.min_size(), self.widgets))
        n = len(self.widgets)
        return (max(w) + 2 * WIDGET_MARGIN, max(h) + (n+1) * WIDGET_MARGIN)

    def on_render(self, dst, rx, ry):
        """
        Render the layout on the given destination at the given position.

        :param dst: The destination surface.
        :param rx: The x position.
        :param ry: The y position.
        """
        x, y = rx + WIDGET_MARGIN, ry + WIDGET_MARGIN
        w, h = zip(*map(lambda x: x.min_size(), self.widgets))
        w, h = max(w), max(h)
        for widget in self.widgets:
            widget.on_render(dst, (x, y, w, h))
            y += h + WIDGET_MARGIN

    def on_event(self, e):
        """
        Process the event.
        """
        for w in self.widgets:
            w.on_event(e)


class HLayout():
    """
    A horizontal layout.
    """

    def __init__(self):
        """
        The __init__ method.
        """
        self.widgets = []

    def size(self):
        """
        Returns the size of the layout.
        """
        w, h = zip(*map(lambda x: x.min_size(), self.widgets))
        n = len(self.widgets)
        return (max(w) + 2 * WIDGET_MARGIN, max(h) + (n+1) * WIDGET_MARGIN)

    def on_render(self, dst, rx, ry):
        """
        Render the layout on the given destination at the given position.

        :param dst: The destination surface.
        :param rx: The x position.
        :param ry: The y position.
        """
        x, y = rx + WIDGET_MARGIN, ry + WIDGET_MARGIN
        w, h = zip(*map(lambda x: x.min_size(), self.widgets))
        w, h = max(w), max(h)
        for widget in self.widgets:
            widget.on_render(dst, (x, y, w, h))
            x += w + WIDGET_MARGIN

    def on_event(self, e):
        """
        Process the event.
        """
        for w in self.widgets:
            w.on_event(e)

class Menu(VLayout):
    """
    A simple menu which calls callbacks on click.
    """
    def __init__(self, *items, cls=Button, **kwargs):
        """
        The __init__ method.

        :param cls: The button class which is to be used.
        :param elements: the items of the menu in the form of (item_name,
            callback)
        :param kwargs: The parameters for the buttons. See the Button
            documentation
        """
        super(Menu, self).__init__()
        self.cls = cls
        for n,c in items:
            self.add_item(n, c, **kwargs)

    def add_item(self, name, callback=lambda : None, **kwargs):
        """
        Adds an item to the menu.

        :param name: The name of the item.
        :param callback: The callback.
        :param kwargs: The parameters for the buttons. See the Button
            documentation
        """
        self.widgets.append(self.cls(**kwargs, text=name, callback=callback))
