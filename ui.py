from inkplate import Inkplate
from layout import TEXT_ALIGN_CENTER, TEXT_ALIGN_RIGHT, FlowLayout

'''
python3 pyboard.py --device /dev/ttyUSB0 -f cp layout.py text.py :
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
        self.root = FlowLayout(
            max_width=width,
            max_height=height,
            padding=20
        )
        nested = FlowLayout(padding=40)
        nested.add_spacer(height // 4)
        self.root.add_node(nested)
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

    def draw(self):
        self.display.clean()
        self.root.draw(self.display, 0, 0)
        self.display.display()


if __name__ == '__main__':
    ui = UI()
    ui.draw()
