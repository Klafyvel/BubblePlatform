"""
The UI module
===============

This module handles everything about the ui : buttons, titles, menus...

Widgets are organizes in layouts.

"""

import pygame
from pygame.locals import *

from bubble_platform.settings import logger
from bubble_platform.pos_in_rect import pos_in_rect

WIDGET_MARGIN = 10
WIDGET_PADDING = 10


class Widget():
    """
    A base class for widgets.
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
        :param min_width: A minimum width for the button. (default = 0)
        :param min_height:A minimum height for the button. (default = 0)
        :param parent: The parent layout. (default = None)

        :type rc_manager: ResourceManager
        :type text: str
        :type color: (int,int,int)
        :type font: str
        :type background: (int, int, int)
        :type border: (int, int, int)
        :type border_width: int
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
        self.min_width = kwargs.get("min_width", 0)
        self.min_height = kwargs.get("min_height", 0)
        self.parent = kwargs.get("parent", None)

        self.rect = (0, 0, 0, 0)
        self.hovered = False
        self.clicked = False
        self.focus = False

    def min_size(self):
        """
        Returns the minimum size the widget needs to be drawn.
        """
        w, h = self.rc_manager.get(self.font).size(self.text)
        return (
            max(self.min_width, w+2*WIDGET_PADDING),
            max(self.min_height, h+2*WIDGET_PADDING)
        )

    def render_border(self, dst):
        if self.border and self.border_width > 0:
            pygame.draw.rect(dst, self.border, self.rect)

    def render_background(self, dst):
        x, y, w, h = self.rect
        if self.background:
            c = self.background
            if self.hovered or self.focus:
                c = (
                    min((c[0]+50), 255),
                    min((c[1]+50), 255),
                    min((c[2]+50), 255),
                )
            rect_bg = (
                x + self.border_width,
                y + self.border_width,
                w - 2*self.border_width,
                h - 2*self.border_width
            )
            pygame.draw.rect(dst, c, rect_bg)

    def render_font(self, dst):
        x, y, w, h = self.rect
        font = self.rc_manager.get(self.font)
        w_f, h_f = font.size(self.text)
        c = self.color
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
            self.focus = pos_in_rect(e.pos, self.rect)
        elif e.type == MOUSEBUTTONUP:
            self.clicked = pos_in_rect(e.pos, self.rect)
            self.focus = self.clicked
        elif e.type == KEYDOWN:
            if self.focus:
                if e.key == K_RETURN:
                    self.clicked = True


class Button(Widget):
    """
    A button in the ui.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the widget documentation.


        :param callback: A function to call when clicked. (default = lambda :
            None)
        """
        super(Button, self).__init__(*args, **kwargs)

        self.callback = kwargs.get("callback", lambda: None)

    def render_background(self, dst):
        x, y, w, h = self.rect
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
                    min((c[0]+50), 255),
                    min((c[1]+50), 255),
                    min((c[2]+50), 255),
                )
            rect_bg = (
                x + self.border_width,
                y + self.border_width,
                w - 2*self.border_width,
                h - 2*self.border_width
            )
            pygame.draw.rect(dst, c, rect_bg)

    def render_font(self, dst):
        x, y, w, h = self.rect
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

    def on_event(self, e):
        """
        Process the event.
        :param e: The event.
        """
        super(Button, self).on_event(e)

        if self.clicked:
            self.callback()
            self.clicked = False


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
        w, h = super(ImageButton, self).min_size()
        w_i, h_i = self.rc_manager.get(self.image).get_size()

        return (w + w_i + WIDGET_PADDING, max(h + 2*WIDGET_PADDING, h_i))

    def render_font(self, dst):
        x, y, w, h = self.rect
        font = self.rc_manager.get(self.font)
        w_label, h_label = font.size(self.text)
        c = self.color
        dst.blit(
            font.render(self.text, True, c),
            (
                x + WIDGET_PADDING,
                y + (h - h_label) / 2
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
                x + (w - w_label) / 2,
                y + (h - image.get_height())/2
            )
        )

    def on_event(self, e):
        """
        Process the event.
        :param e: The event.
        """
        super(Input, self).on_event(e)

        if e.type == MOUSEBUTTONDOWN:
            self.clicked = pos_in_rect(e.pos, self.rect)
        elif e.type == MOUSEBUTTONUP:
            self.clicked = False
            if pos_in_rect(e.pos, self.rect):
                self.callback()


class Input(Widget):
    """
    A simple input widget.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the Widget documentation.

        :param max_length: The maximum length of the input string. (default=None)

        """
        super(Input, self).__init__(*args, **kwargs)

        self.max_length = kwargs.get("max_length", None)

        self.input = ""

    def min_size(self):
        w_label, h_label = self.rc_manager.get(self.font).size(self.text)
        font = self.rc_manager.get(self.font)
        if self.max_length:
            w_input, h_input = font.size('H'*self.max_length)
        else:
            w_input, h_input = font.size(self.input)
        return (
            w_label + w_input + 3*WIDGET_PADDING,
            h_label + h_input + 3*WIDGET_PADDING
        )

    def render_font(self, dst):
        x, y, w, h = self.rect
        font = self.rc_manager.get(self.font)
        w_label, h_label = font.size(self.text)
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
                x + WIDGET_PADDING,
                y + (h - h_label) / 2
            )
        )
        w_input, h_input = font.size(self.input)
        dst.blit(
            font.render(self.input, True, c),
            (
                x + 2*WIDGET_PADDING + w_label +
                (w - 2*WIDGET_PADDING - w_label - w_input)/2,
                y + (h - h_input)/2
            )
        )

    def on_event(self, e):
        """
        Process the event.
        :param e: The event.
        """
        super(Input, self).on_event(e)

        if self.focus:
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:
                    self.input = self.input[:-1]
                elif self.max_length and (e.unicode.isalnum() or (e.unicode in ' _.')):
                    if len(self.input) < self.max_length:
                        self.input += e.unicode
                elif e.unicode.isalnum():
                    self.input += e.unicode

class Layout():
    """
    The base class for layouts.
    """
    def __init__(self, *widgets):
        """
        The __init__ method.

        :param widgets: the widgets to be added.
        """
        self.widgets = list(widgets)

    def size(self):
        """
        Returns the size of the layout.
        """
        return (0,0)

    def on_render(self, dst, rx, ry):
        """
        Render the layout on the given destination at the given position.

        :param dst: The destination surface.
        :param rx: The x position.
        :param ry: The y position.
        """
        pass

    def on_event(self, e):
        """
        Process the event.
        """
        for w in self.widgets:
            w.on_event(e)

    def add_widget(self, w):
        """
        Adds a widget to the layout.

        :param w: The widget.
        """
        w.parent = self
        self.widgets.append(w)

    def on_next(self):
        """
        Focus the next widget in the widget list.
        """
        logger.debug("Next")
        current = -1
        for i,w in enumerate(self.widgets):
            if w.focus:
                current = i
                w.focus = False
                break

        self.widgets[(current + 1)%len(self.widgets)].focus = True

    def on_previous(self):
        """
        Focus the previous widget in the widget list.
        """
        logger.debug("Previous")
        current = -1
        for i,w in enumerate(self.widgets):
            if w.focus:
                current = i
                w.focus = False
                break

        self.widgets[(current - 1)%len(self.widgets)].focus = True


class VLayout(Layout):
    """
    A vertical layout.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the Layout documentation.
        """
        super(VLayout, self).__init__(*args, **kwargs)

    def size(self):
        """
        Returns the size of the layout.
        """
        w, h = zip(*map(lambda x: x.min_size(), self.widgets))
        n = len(self.widgets)
        return (max(w) + 2 * WIDGET_MARGIN, max(h)*n + (n+1) * WIDGET_MARGIN)

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



class HLayout(Layout):
    """
    A horizontal layout.
    """

    def __init__(self, *args, **kwargs):
        """
        The __init__ method.

        See the Layout documentation.
        """
        super(HLayout, self).__init__(*args, **kwargs)


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
