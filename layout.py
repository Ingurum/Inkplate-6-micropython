from text import Text

# Text alignments

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_CENTER = 1
TEXT_ALIGN_RIGHT = 2


class Node:
    '''
    A layout node.
    '''

    def __init__(self, padding=0):
        self.padding = padding

    def measure(self):
        '''
        Return the measured dimensions.
        '''
        return None, None

    def draw(self, display, x, y):
        pass


class FlowLayout(Node):
    '''
    A simple FlowLayout. 
    '''

    def __init__(
            self,
            max_width=0,
            max_height=0,
            parent=None,
            padding=0):

        super().__init__(padding=padding)
        self.parent = parent
        self.max_width = max_width - 2 * self.padding
        self.max_height = max_height - 2 * self.padding
        self.children = list()

    def add_node(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def add_spacer(self, height):
        node = Spacer(parent=self, height=height)
        self.add_node(node)

    def add_text_content(self, content, text_size=3, align=TEXT_ALIGN_LEFT):
        node = TextNode(
            parent=self,
            content=content,
            text_size=text_size,
            align=align
        )
        self.add_node(node)

    def measure(self):
        if self.parent:
            width = self.max_width
            height = self.max_height
            return width, height
        else:
            width = 0
            height = 0
            for child in self.children:
                if child is Node:
                    w, h = child.measure()
                    width += w
                    height += h

            width += 2 * self.padding
            height += 2 * self.padding
            return width, height

    def draw(self, display, x, y):
        d_x = x + self.padding
        d_y = y + self.padding

        for child in self.children:
            _, h = child.measure()
            child.draw(display, d_x, d_y)
            d_y += h


class TextNode(Node):
    '''
    A Text Node.
    '''

    def __init__(
            self,
            parent,
            content,
            text_size=3,
            padding=5,
            align=TEXT_ALIGN_LEFT):

        super().__init__(padding=padding)
        self.parent = parent
        self.content = content
        self.max_width = getattr(parent, 'max_width', 0)
        self.text_size = text_size
        self.text = Text(
            self.content,
            text_size=self.text_size,
            padding=self.padding
        )
        self.align = align

    def measure(self):
        return self.text.measured_width(), self.text.measured_height()

    def draw(self, display, x, y):
        d_x = x
        d_y = y + self.padding
        if self.align == TEXT_ALIGN_CENTER or self.align == TEXT_ALIGN_RIGHT:
            if self.max_width == 0:
                print('Invalid constraints [TextNode %s]' % (self.content))
            else:
                width = self.text.measured_width()
                half_width = int(width / 2)
                if self.align == TEXT_ALIGN_CENTER:
                    d_x = int(self.max_width / 2) - half_width
                else:
                    d_x = self.max_width - width
        else:
            d_x = x + self.padding

        # Debug
        display.drawRect(
            x,
            y,
            self.max_width,
            self.text.measured_height() + self.padding,
            display.BLACK
        )
        display.setTextSize(self.text_size)
        display.printText(
            d_x,
            d_y,
            self.text.content
        )


class Spacer(Node):
    '''
    A Spacer that represents an empty space.
    '''

    def __init__(self, parent, height):
        super().__init__(padding=0)
        self.parent = parent
        self.max_width = getattr(parent, 'max_width', 0)
        self.height = height

    def measure(self):
        return self.max_width, self.height

    def draw(self, display, x, y):
        # Debug
        display.drawRect(
            x,
            y,
            self.max_width,
            self.height,
            display.BLACK
        )
