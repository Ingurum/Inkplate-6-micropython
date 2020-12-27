_WIDTHS = {
    1:  8,
    2:  10,
    3:  18,
    4:  25,
    5:  30,
    6:  35,
    7:  45,
    8:  50,
    9:  55,
    10: 55,
}

_HEIGHTS = {
    1:  10,
    2:  15,
    3:  25,
    4:  30,
    5:  40,
    6:  50,
    7:  50,
    8:  60,
    9:  70,
    10: 80,
}


class Text:
    '''
    A class that helps with text rendering. 
    Allows justifying text because it knows how to measure itself.
    '''

    def __init__(self, content, text_size=2, padding=5):
        self.content = content.upper()
        self.length = len(content)
        text_size = 1 if (text_size < 1) else text_size
        text_size = 10 if (text_size > 10) else text_size
        self.text_size = text_size
        self.padding = padding

    def measured_width(self):
        return self.length * _WIDTHS[self.text_size] + 2 * self.padding

    def measured_height(self):
        return _HEIGHTS[self.text_size] + 2 * self.padding
