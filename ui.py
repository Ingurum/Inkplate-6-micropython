from images import CALENDAR_40_40
from inkplate import Inkplate
from layout import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, Column, Row

'''
python pyboard.py --device /dev/ttyUSB0 -f cp layout.py text.py images.py :
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
        self._build_calendar(width, height)

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
        row = Row(parent=self.root, padding=10, align=ALIGN_CENTER)
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
            align=ALIGN_CENTER
        )
        self.root.add_text_content(
            'More Medium Text',
            text_size=5,
            align=ALIGN_RIGHT
        )
        self.root.add_text_content(
            'Large Text',
            text_size=9,
            align=ALIGN_CENTER
        )
        self.root.add_text_content(
            'Largest Text',
            text_size=10,
            align=ALIGN_CENTER
        )

    def _columnar_interface(self, width, height):
        self.root = Row(
            layout_width=width,
            layout_height=height,
            padding=5,
            align=ALIGN_CENTER
        )

        count = 3
        columns = [
            Column(
                self.root,
                layout_width=width // count,
                wrap_content=False,  # Fill parent
                padding=10,
                outline=True)
            for _ in range(count)
        ]
        for column in columns:
            column.add_text_content('Line 1', align=ALIGN_CENTER)
            column.add_text_content('Line 2', align=ALIGN_CENTER)
            column.add_text_content('Line 3', align=ALIGN_CENTER)
            column.add_text_content('Line 4', align=ALIGN_CENTER)
            column.add_text_content('Line 5', align=ALIGN_RIGHT)
            column.add_text_content('Line 6', align=ALIGN_LEFT)
            column.add_image(CALENDAR_40_40, 40,  40, align=ALIGN_CENTER)
            self.root.add_node(column)

    def _build_calendar(self, width, height):
        self.root = Column(
            layout_width=width,
            layout_height=height,
            padding=20
        )
        row = Row(
            parent=self.root,
            layout_height=40,
            wrap_content=False
        )
        row.add_text_content('Calendar', text_size=4)
        row.add_image(CALENDAR_40_40, 40, 40, align=ALIGN_RIGHT)
        content = Row(
            parent=self.root,
            layout_height=440,
            wrap_content=False,
            outline=True
        )
        content.add_spacer(10, outline=True)
        status = Row(
            parent=self.root,
            layout_height=40,
            wrap_content=False,
            outline=True
        )
        status.add_text_content('Last updated at <>', align=ALIGN_RIGHT)
        self.root.add_node(row)
        self.root.add_node(content)
        self.root.add_node(status)

    def draw(self):
        self.display.clean()
        self.root.draw(self.display, 0, 0)
        self.display.display()


if __name__ == '__main__':
    ui = UI()
    ui.draw()
