from text import Text

# Text alignments

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_CENTER = 1
TEXT_ALIGN_RIGHT = 2


class Node:
    '''
    A layout node.
    '''

    def __init__(self, parent=None, padding=0):
        self.parent = parent
        self.padding = padding

    def max_width(self):
        if self.parent:
            return self.parent.max_width()
        else:
            return getattr(self, 'm_width', 0) - 2 * self.padding

    def max_height(self):
        if self.parent:
            return self.parent.max_height()
        else:
            return getattr(self, 'm_height', 0) - 2 * self.padding

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

    def __init__(self, parent=None, m_width=0, m_height=0, padding=0):
        super().__init__(parent=parent, padding=padding)
        if parent:
            self.m_width = self.max_width()
            self.m_height = self.max_height()
        else:
            self.m_width = m_width
            self.m_height = m_height
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
        width = self.m_width
        height = 0
        for child in self.children:
            if child is Node:
                _, h = child.measure()
                height += h

        height += 2 * self.padding
        return width, height

    def draw(self, display, x, y):
        d_x = x + self.padding
        d_y = y

        for child in self.children:
            _, h = child.measure()
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
        self.m_width = self.max_width()
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
            if self.m_width == 0:
                print('Invalid constraints [TextNode %s]' % (self.content))
            else:
                width = self.text.measured_width()
                half_width = int(width / 2)
                if self.align == TEXT_ALIGN_CENTER:
                    d_x = int(self.m_width / 2) - half_width
                else:
                    d_x = self.m_width - width
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

    def __init__(self, parent=None, m_width=0, m_height=0, padding=0):
        super().__init__(parent=parent, padding=padding)
        if parent:
            self.m_width = self.max_width()
            self.m_height = self.max_height()
        else:
            self.m_width = m_width
            self.m_height = m_height
        self.children = list()

    def measure(self):
        width = self.m_width
        height = 0
        for child in self.children:
            if child is Node:
                _, h = child.measure()
                height = h if height < h else height

        height += 2 * self.padding
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
        d_y = y
        for child in self.children:
            w, _ = child.measure()
            child.draw(display, d_x, d_y)
            d_x += w + self.padding


class Spacer(Node):
    '''
    A Spacer that represents an empty space.
    '''

    def __init__(self, parent, height, padding=0):
        super().__init__(parent=parent, padding=padding)
        self.width = self.max_width()
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
