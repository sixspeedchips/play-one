

class Position:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self) -> str:
        return "[" + str(self.x) + ", " + str(self.y) + "]"

