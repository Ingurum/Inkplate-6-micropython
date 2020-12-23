from inkplate import Inkplate
from layout import TEXT_ALIGN_CENTER, TEXT_ALIGN_LEFT, TEXT_ALIGN_RIGHT, Column, Row

'''
python pyboard.py --device /dev/ttyUSB0 -f cp layout.py text.py :
python pyboard.py --device /dev/ttyUSB0 ui.py
'''


class UI:
    '''
    This helps with layout of the InkPlate UI. 
    Everything is rendered via immediate mode & everything is being re-rendered
    via partial updates.
    '''

    def __init__(self):
        self.display = Inkplate(Inkplate.INKPLATE_1BIT)
        self.display.begin()
        width = self.display.width()
        height = self.display.height()
        self._columnar_interface(width, height)

    def _build_textual_interface(self, width, height):
        self.root = Column(
            layout_width=width,
            layout_height=height,
            padding=20
        )
        # Nested Column
        column = Column(parent=self.root, padding=0)
        column.add_spacer(20)
        self.root.add_node(column)
        # Nested Row
        row = Row(parent=self.root, padding=10)
        row.add_text_content('Test 1')
        row.add_text_content('Test 2')
        row.add_text_content('Test 3')
        row.add_text_content('Test 4')
        self.root.add_node(row)
        # Other text nodes
        self.root.add_text_content(
            'Good Morning, Rahul',
            text_size=3
        )
        self.root.add_text_content('Some text')
        self.root.add_text_content('Some more text')
        self.root.add_text_content(
            'Medium Text',
            text_size=5,
            align=TEXT_ALIGN_CENTER
        )
        self.root.add_text_content(
            'More Medium Text',
            text_size=5,
            align=TEXT_ALIGN_RIGHT
        )
        self.root.add_text_content(
            'Large Text',
            text_size=9,
            align=TEXT_ALIGN_CENTER
        )
        self.root.add_text_content(
            'Largest Text',
            text_size=10,
            align=TEXT_ALIGN_CENTER
        )

    def _columnar_interface(self, width, height):
        self.root = Row(
            layout_width=width,
            layout_height=height,
            padding=15
        )

        count = 3
        columns = [
            Column(
                self.root,
                layout_width=width // count,
                padding=10) for _ in range(count)
        ]
        for column in columns:
            column.add_text_content('Line 1', align=TEXT_ALIGN_CENTER)
            column.add_text_content('Line 2', align=TEXT_ALIGN_CENTER)
            column.add_text_content('Line 3', align=TEXT_ALIGN_CENTER)
            column.add_text_content('Line 4', align=TEXT_ALIGN_CENTER)
            column.add_text_content('Line 5', align=TEXT_ALIGN_RIGHT)
            column.add_text_content('Line 6', align=TEXT_ALIGN_LEFT)
            self.root.add_node(column)

    def draw(self):
        self.display.clean()
        self.root.draw(self.display, 0, 0)
        self.display.display()


if __name__ == '__main__':
    ui = UI()
    ui.draw()
