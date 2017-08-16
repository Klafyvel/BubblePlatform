"""
The pos_in_rect_module provides the pos_in_rect function which allows user to
check if (x,y) is in the rectangle (x,y,w,h).
"""

def pos_in_rect(pos, rect):
    """
    allow to check if (x,y) is in the rectangle (x,y,w,h)

    :param pos: the (x,y), position.
    :param rect: the (x,y,w,h) rectangle.
    """
    x,y = pos
    return (rect[0] <= x <= rect[0] + rect[2]) and (rect[1] <= y <= rect[1] + rect[3])