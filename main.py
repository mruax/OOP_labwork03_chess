import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from chess import Pawn, Rook, Bishop, Knight, Queen, King, Chip
from generated_ui import Ui_Dialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Chess game")
        icon = QIcon(str(Path("src/chess.ico")))
        self.setWindowIcon(icon)

        # manually added fixed headers size restriction
        self.ui.field.horizontalHeader().setMinimumSectionSize(68)
        self.ui.field.horizontalHeader().setMaximumSectionSize(68)
        self.ui.field.verticalHeader().setMinimumSectionSize(68)
        self.ui.field.verticalHeader().setMaximumSectionSize(68)


def create_figure(x, y, table, image, color):
    """
    Creates figure

    :param x: coordinate from 0 to 7
    :param y: coordinate from 0 to 7
    :param table: window.ui.field
    :param image: black or white QPixmap
    :param color: QColor(0-255, 0-255, 0-255)
    :return: None
    """
    item = QTableWidgetItem()
    item.setData(Qt.ItemDataRole.DecorationRole, image)
    item.setBackground(color)
    table.setItem(x, y, item)


def default_color(x, y):
    res = QColor(0, 0, 0)
    if (x + y) % 2 != 1:
        res = QColor(255, 255, 255)
    return res


def rook_moves(x, y):
    """
    Function returns list of all possible rook moves [[x1, y1], [x2, y2], ...]

    :param x: figure x coordinate
    :param y: figure y coordinate
    :return: list
    """
    res = []
    if x != 7:  # if not bottom line
        for i in range(x + 1, 7 + 1):
            t = field[i][y]
            res.append([i, y])
            if t:  # if figure found, adds it (because it can be opponent figure) and stopped
                break
    if x != 0:  # if not upper line
        for i in range(x - 1, 0 - 1, -1):
            t = field[i][y]
            res.append([i, y])
            if t:  # figure found
                break
    if y != 7:  # if not right line
        for j in range(y + 1, 7 + 1):
            t = field[x][j]
            res.append([x, j])
            if t:  # figure found
                break
    if y != 0:  # if not left line
        for j in range(y - 1, 0 - 1, -1):
            t = field[x][j]
            res.append([x, j])
            if t:  # figure found
                break
    return res


def bishop_moves(x, y):
    """
    Function returns list of all possible bishop moves [[x1, y1], [x2, y2], ...]

    :param x: figure x coordinate
    :param y: figure y coordinate
    :return: list
    """
    res = []
    left_upper, left_bottom, right_upper, right_bottom = False, False, False, False
    if x == 0:
        left_upper = True
        right_upper = True
    if x == 7:
        left_bottom = True
        right_bottom = True
    if y == 0:
        left_upper = True
        left_bottom = True
    if y == 7:
        right_upper = True
        right_bottom = True
    if not left_upper:
        for i in range(1, 7 + 1):
            if not (0 <= x - i <= 7 and 0 <= y - i <= 7):
                break
            t = field[x - i][y - i]
            res.append([x - i, y - i])
            if t:
                break
    if not left_bottom:
        for i in range(1, 7 + 1):
            if not (0 <= x + i <= 7 and 0 <= y - i <= 7):
                break
            t = field[x + i][y - i]
            res.append([x + i, y - i])
            if t:
                break
    if not right_upper:
        for i in range(1, 7 + 1):
            if not (0 <= x - i <= 7 and 0 <= y + i <= 7):
                break
            t = field[x - i][y + i]
            res.append([x - i, y + i])
            if t:
                break
    if not right_bottom:
        for i in range(1, 7 + 1):
            if not (0 <= x + i <= 7 and 0 <= y + i <= 7):
                break
            t = field[x + i][y + i]
            res.append([x + i, y + i])
            if t:
                break
    return res


def knight_moves(x, y):
    """
    Function returns list of all possible knight moves [[x1, y1], [x2, y2], ...]

    :param x: figure x coordinate
    :param y: figure y coordinate
    :return: list
    """
    res = []
    moves = [[1, 2], [2, 1], [-1, -2], [-2, -1], [-1, 2], [2, -1], [1, -2], [-2, 1]]
    for i in range(8):
        if 0 <= x + moves[i][0] <= 7 and 0 <= y + moves[i][1] <= 7:
            res.append([x + moves[i][0], y + moves[i][1]])
    return res


def queen_moves(x, y):
    """
    Function returns list of all possible queen moves [[x1, y1], [x2, y2], ...]

    :param x: figure x coordinate
    :param y: figure y coordinate
    :return: list
    """
    res1 = rook_moves(x, y)
    res2 = bishop_moves(x, y)
    return res1 + res2


def show_possible_items(cells, table, color):
    for cell in cells:
        check_cell = field[cell[0]][cell[1]]
        if check_cell:  # If figure in cell
            if check_cell.color == color:  # and same color
                continue  # No move
            else:  # possible attack move
                create_figure(cell[0], cell[1], table, check_cell.image, QColor(240, 80, 0))
        else:  # free cell move
            create_figure(cell[0], cell[1], table, QPixmap, QColor(240, 240, 0))


def start_positions(table):
    pass


def init_field_matrix(field):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # Figure pixmaps
    figure_size = QSize(63, 63)
    pawn_pixmap = QPixmap(str(Path("src/pawn.png")))
    pawn_pixmap = pawn_pixmap.scaled(figure_size)
    white_pawn_pixmap = QPixmap(str(Path("src/white_pawn.png")))
    white_pawn_pixmap = white_pawn_pixmap.scaled(figure_size)
    rook_pixmap = QPixmap(str(Path("src/rook.png")))
    rook_pixmap = rook_pixmap.scaled(figure_size)
    white_rook_pixmap = QPixmap(str(Path("src/white_rook.png")))
    white_rook_pixmap = white_rook_pixmap.scaled(figure_size)
    bishop_pixmap = QPixmap(str(Path("src/bishop.png")))
    bishop_pixmap = bishop_pixmap.scaled(figure_size)
    white_bishop_pixmap = QPixmap(str(Path("src/white_bishop.png")))
    white_bishop_pixmap = white_bishop_pixmap.scaled(figure_size)
    knight_pixmap = QPixmap(str(Path("src/knight.png")))
    knight_pixmap = knight_pixmap.scaled(figure_size)
    white_knight_pixmap = QPixmap(str(Path("src/white_knight.png")))
    white_knight_pixmap = white_knight_pixmap.scaled(figure_size)
    queen_pixmap = QPixmap(str(Path("src/queen.png")))
    queen_pixmap = queen_pixmap.scaled(figure_size)
    white_queen_pixmap = QPixmap(str(Path("src/white_queen.png")))
    white_queen_pixmap = white_queen_pixmap.scaled(figure_size)
    king_pixmap = QPixmap(str(Path("src/king.png")))
    king_pixmap = king_pixmap.scaled(figure_size)
    white_king_pixmap = QPixmap(str(Path("src/white_king.png")))
    white_king_pixmap = white_king_pixmap.scaled(figure_size)

    red_chip_pixmap = QPixmap(str(Path("src/red_chip.png")))
    red_chip_pixmap = red_chip_pixmap.scaled(figure_size)
    blue_chip_pixmap = QPixmap(str(Path("src/blue_chip.png")))
    blue_chip_pixmap = blue_chip_pixmap.scaled(figure_size)

    # Matrix with class objects
    field = [[0 for j in range(8)] for i in range(8)]
    # init_field_matrix(field)

    # Show figures on board
    # start_positions(window.ui.field)

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    task = int(input("Введите номер задания (1, 2, 3) - "))
    # k = x1, l = y1, m = x2, n = y2
    print("Введите k, l, m, n (k и m - числа, l и n - буква):")
    x1, y1 = int(input("k = ")), alphabet.index(input("l = "))
    x2, y2 = int(input("m = ")), alphabet.index(input("n = "))
    x1 -= 1
    x2 -= 1
    color1 = default_color(x1, y1)
    color2 = default_color(x2, y2)
    match task:
        case 1:
            chip1 = Chip(x1, y1, 0, red_chip_pixmap)
            chip2 = Chip(x2, y2, 1, blue_chip_pixmap)
            create_figure(x1, y1, window.ui.field, red_chip_pixmap, color1)
            create_figure(x2, y2, window.ui.field, blue_chip_pixmap, color2)
            field[x1][y1] = chip1
            field[x2][y2] = chip2
            if color1 == color2:
                print("Цвет клетки совпадает!")
            else:
                print("Цвет клеток разный!")
        case 2:
            chip = Chip(x2, y2, 1, blue_chip_pixmap)
            create_figure(x2, y2, window.ui.field, blue_chip_pixmap, color2)
            field[x2][y2] = chip
            num = int(input("Выберите номер фигуры (1=ферзь, 2=ладья, 3=слон) - "))
            match num:
                case 1:
                    figure = Queen(x1, y1, 0, queen_pixmap)
                    create_figure(x1, y1, window.ui.field, queen_pixmap, color1)
                    field[x1][y1] = figure
                    cells = queen_moves(x1, y1)
                case 2:
                    figure = Rook(x1, y1, 0, rook_pixmap)
                    create_figure(x1, y1, window.ui.field, rook_pixmap, color1)
                    field[x1][y1] = figure
                    cells = rook_moves(x1, y1)
                case 3:
                    figure = Bishop(x1, y1, 0, bishop_pixmap)
                    create_figure(x1, y1, window.ui.field, bishop_pixmap, color1)
                    field[x1][y1] = figure
                    cells = bishop_moves(x1, y1)
            show_possible_items(cells, window.ui.field, 0)
            flag = False
            for x, y in cells:
                if x == x2 and y == y2:
                    flag = True
                    break
            if flag:
                print("Пересечение есть!")
            else:
                print("Пересечения нет :(")
        case 3:
            pass

    window.show()
    sys.exit(app.exec())
