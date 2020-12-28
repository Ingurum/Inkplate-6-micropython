import time

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
        self.width = self.display.width()
        self.height = self.display.height()
        self._columnar_interface()

    def _build_textual_interface(self):
        self.root = Column(
            layout_width=self.width,
            layout_height=self.height,
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

    def _columnar_interface(self):
        self.root = Row(
            layout_width=self.width,
            layout_height=self.height,
            padding=5,
            align=ALIGN_CENTER
        )

        count = 3
        columns = [
            Column(
                self.root,
                layout_width=self.width // count,
                wrap_content=False,  # Fill parent
                padding=10,
                outline=True)
            for _ in range(count)
        ]
        for column in columns:
            column.add_text_content('Line 1 happens to be long', align=ALIGN_CENTER)
            column.add_text_content('Line 2', align=ALIGN_CENTER)
            column.add_text_content('Line 3', align=ALIGN_CENTER)
            column.add_text_content('Line 4', align=ALIGN_CENTER)
            column.add_text_content('Line 5', align=ALIGN_RIGHT)
            column.add_text_content('Line 6', align=ALIGN_LEFT)
            column.add_image(CALENDAR_40_40, 40,  40, align=ALIGN_CENTER)
            self.root.add_node(column)

    def _build_calendar(self):
        self.root = Column(
            layout_width=self.width,
            layout_height=self.height,
            padding=20
        )
        header = Row(
            parent=self.root,
            layout_height=40,
            wrap_content=False
        )
        header.add_text_content('Calendar', text_size=4)
        header.add_image(CALENDAR_40_40, 40, 40, align=ALIGN_RIGHT)
        content_root = Row(
            parent=self.root,
            layout_height=440,
            wrap_content=False,
            outline=True
        )
        content = Column(
            parent=content_root,
            wrap_content=False
        )
        content.add_spacer(10, outline=True)
        content_root.add_node(content)
        status = Row(
            parent=self.root,
            layout_height=40,
            wrap_content=False,
            outline=True
        )
        status.add_text_content('Last updated at <>', align=ALIGN_RIGHT)
        self.root.add_node(header)
        self.root.add_node(content_root)
        self.root.add_node(status)

    def _build_auth(self):
        self.root = Column(
            layout_width=self.width,
            layout_height=self.height,
            padding=10
        )
        header = Row(
            parent=self.root,
            layout_height=40,
            wrap_content=False
        )
        header.add_text_content('Calendar', text_size=4)
        header.add_image(CALENDAR_40_40, 40, 40, align=ALIGN_RIGHT)
        content_root = Row(
            parent=self.root,
            layout_height=520,
            wrap_content=False,
            outline=True
        )
        content = Column(
            parent=content_root,
            wrap_content=False
        )
        content.add_spacer(10, outline=True)
        content.add_spacer(self.width // 4)
        content.add_text_content('ABCD-EFGH', text_size=6, align=ALIGN_CENTER)
        content.add_text_content(
            'google.com/auth/code to continue',
            align=ALIGN_CENTER
        )
        content_root.add_node(content)
        self.root.add_node(header)
        self.root.add_node(content_root)

    def draw(self):
        self.display.clearDisplay()
        self.root.draw(self.display, 0, 0)
        self.display.display()


if __name__ == '__main__':
    ui = UI()
    ui.draw()
    time.sleep(5)
    ui._build_auth()
    ui.draw()
    time.sleep(5)
    ui._build_calendar()
    ui.draw()
    time.sleep(5)
