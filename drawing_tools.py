
class DrawingTool:
    def __init__(self, newSize, newColor):
        self._size = newSize
        self._color = newColor

    def configure(self, **kwargs):
        """ Update the size and color of the tool """
        if "size" in kwargs:
            self._size = kwargs['size']
        
        if "color" in kwargs:
            self._color = kwargs['color']
        

class Pencil(DrawingTool):
    def __init__(self, size, color):
        DrawingTool.__init__(self, size, color)
        
    def create(self, canvas, oldX: int, oldY: int, newX: int, newY: int):
        """Draw a line from the previous known location of the mouse
            to its current location.
        """
        canvas.create_line(oldX, oldY, newX, newY,
                                fill = self._color)

class Brush(DrawingTool):
    def __init__(self, size, color):
        DrawingTool.__init__(self, size, color)

    def create(self, canvas, oldX: int, oldY: int, newX: int, newY: int):
        """Draw a cirlce using mouse location as the center
        """
        topX = newX - self._size/2
        topY = newY - self._size/2
        bottomX = newX + self._size/2
        bottomY = newY + self._size/2
        canvas.create_oval(topX, topY, bottomX, bottomY,
                           fill = self._color,
                           outline = "")


class Square(DrawingTool):
    def __init__(self, size, color):
        DrawingTool.__init__(self, size, color)

    def create(self, canvas, oldX: int, oldY: int, newX: int, newY: int):
        """Draw a square from the x and y coordinates of the original click
        point, to the mouse's new location.
        """
        identity = canvas.create_rectangle(oldX, oldY, newX, newY,
                                           fill = self._color,
                                           outline = "")
        return identity


class Circle(DrawingTool):
    def __init__(self, size, color):
        DrawingTool.__init__(self, size, color)

    def create(self, canvas, oldX: int, oldY: int, newX: int, newY: int):
        """Draw an oval from the x and y coordinates of the original click
        point, to the mouse's new location.
        """
        identity = canvas.create_oval(oldX, oldY, newX, newY,
                                      fill = self._color,
                                      outline = "")
        return identity


class Triangle(DrawingTool):
    def __init__(self, size, color):
        DrawingTool.__init__(self, size, color)

    def create(self, canvas, oldX:int, oldY: int, newX: int, newY: int):
        """Draw an triangle from the x and y coordinates of the original click
        point, to the mouse's new location.
        """
        v1x = oldX
        v1y = oldY
        v2x = oldX - (newX-oldX)
        v2y = newY
        v3x = newX
        v3y = newY

        identity = canvas.create_polygon(v1x, v1y, v2x, v2y, v3x, v3y,
                                         fill = self._color)
        return identity

