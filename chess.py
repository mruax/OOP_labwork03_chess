class Figure:
    def __init__(self, x, y, color, image):
        self.x = x  # [0..7]
        self.y = y  # [0..7]
        self.color = color  # 0 - Black, 1 - White
        self.image = image  # QPixmap

    def move(self, x, y):
        self.x = x
        self.y = y


class Pawn(Figure):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.first_move = True

    def __repr__(self):
        return "P"


class Rook(Figure):
    def __repr__(self):
        return "R"


class Bishop(Figure):
    def __repr__(self):
        return "B"


class Knight(Figure):
    def __repr__(self):
        return "K"


class Queen(Figure):
    def __repr__(self):
        return "Q"


class King(Figure):
    def __repr__(self):
        return "+"


class Chip(Figure):
    def __repr__(self):
        return "C"
