from inkplate import Inkplate

display = Inkplate(Inkplate.INKPLATE_1BIT)
width = display.width()
height = display.height()

if __name__ == "__main__":
    # Must be called before using, line in Arduino
    display.begin()

    for i in range(0, height, 10):
        display.drawFastHLine(0, i, width, display.BLACK)

    for i in range(0, width, 10):
        display.drawFastVLine(i, 0, height, display.BLACK)
    
    y = 10
    for i in range(1, 11, 1):
        display.setTextSize(i)
        display.printText(10, y, 'Hello World'.upper())
        y += 9 * i
    
    display.display()
