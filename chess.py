class Figure:
    def __init__(self, x, y, color):
        self.x = x  # [0..7]
        self.y = y  # [0..7]
        self.color = color  # 0 - Black, 1 - White

    def move(self, x, y):
        self.x = x
        self.y = y


class Pawn(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.first_move = True

    def possible_moves(self):
        c = [1, 2]  # c - coefficients
        if self.color == 1:
            c = [-1, -2]

        if self.first_move:
            return [[self.x, self.y + c[0]],
                    [self.x, self.y + c[1]]]
        return [self.x, self.y + c[0]]

    def move(self, x, y):
        super().move(x, y)
        if y == 0 or y == 7:
            pass  # TODO: convert to queen
