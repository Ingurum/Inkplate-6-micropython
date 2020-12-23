from text import Text

# Text alignments

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_CENTER = 1
TEXT_ALIGN_RIGHT = 2


class Node:
    '''
    A layout node.
    '''

    def __init__(self, parent=None, layout_width=0, layout_height=0, padding=0):
        self.parent = parent
        self.padding = padding
        if not self.parent and (layout_width == 0 or layout_height == 0):
            raise RuntimeError(
                'Invalid constraints. Must specify parent or a size.')

        if self.parent and layout_width == 0:
            self.layout_width = self.parent.layout_width
        else:
            self.layout_width = layout_width

        if self.parent and layout_height == 0:
            self.layout_height = self.parent.layout_height
        else:
            self.layout_height = layout_height

        self.layout_width -= 2 * self.padding
        self.layout_height -= 2 * self.padding

    def measure(self):
        '''
        Return the measured dimensions.
        '''
        return None, None

    def draw(self, display, x, y):
        pass


class Column(Node):
    '''
    A simple FlowLayout. 
    '''

    def __init__(self, parent=None, layout_width=0, layout_height=0, padding=0):
        super().__init__(
            parent=parent,
            layout_width=layout_width,
            layout_height=layout_height,
            padding=padding
        )
        self.children = list()

    def add_node(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def add_spacer(self, height):
        node = Spacer(self, height)
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
        width = self.layout_width
        height = 0
        for child in self.children:
            if child is Node:
                _, h = child.measure()
                height += h

        if height == 0:
            height = self.layout_height
        else:
            height += self.padding
        return width, height

    def draw(self, display, x, y):
        d_x = x + self.padding
        d_y = y + self.padding

        for child in self.children:
            w, h = child.measure()
            child.draw(display, d_x, d_y)
            d_y += h + self.padding


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

        super().__init__(parent=parent, padding=padding)
        self.content = content
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
            if self.layout_width == 0:
                print('Invalid constraints [TextNode %s]' % (self.content))
            else:
                width = self.text.measured_width()
                half_width = int(width / 2)
                if self.align == TEXT_ALIGN_CENTER:
                    d_x = x + (int(self.layout_width / 2) - half_width)
                else:
                    d_x = x + (self.layout_width - width)
        else:
            d_x = x + self.padding
        display.setTextSize(self.text_size)
        display.printText(
            d_x,
            d_y,
            self.text.content
        )


class Row(Node):
    '''
    A Row. (Flow layout in horizontal direction)
    '''

    def __init__(self, parent=None, layout_width=0, layout_height=0, padding=0):
        super().__init__(
            parent=parent,
            layout_width=layout_width,
            layout_height=layout_height,
            padding=padding
        )
        self.children = list()

    def measure(self):
        width = self.layout_width
        height = 0
        for child in self.children:
            if child is Node:
                _, h = child.measure()
                height = h if height < h else height

        if height == 0:
            height = self.layout_height
        else:
            height += self.padding

        return width, height

    def add_node(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def add_spacer(self, height):
        node = Spacer(self, height, padding=self.padding)
        self.add_node(node)

    def add_text_content(self, content, text_size=3, align=TEXT_ALIGN_LEFT):
        node = TextNode(
            parent=self,
            content=content,
            text_size=text_size,
            align=align
        )
        self.add_node(node)

    def draw(self, display, x, y):
        d_x = x + self.padding
        d_y = y + self.padding
        for child in self.children:
            w, h = child.measure()
            # Debug
            display.drawRect(d_x, d_y, w, h, display.BLACK)
            child.draw(display, d_x, d_y)
            d_x += w + self.padding


class Spacer(Node):
    '''
    A Spacer that represents an empty space.
    '''

    def __init__(self, parent, height, padding=0):
        super().__init__(parent=parent, padding=padding)
        self.width = self.layout_width
        self.height = height

    def measure(self):
        return self.width, self.height

    def draw(self, display, x, y):
        # Debug
        display.drawRect(
            x,
            y,
            self.width,
            self.height,
            display.BLACK
        )
