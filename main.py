import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from generated_ui import Ui_Dialog
from chess import Pawn, Rook, Bishop, Knight, Queen


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

        self.ui.field.itemSelectionChanged.connect(self.onItemSelected)
        self.ui.turn_button.clicked.connect(self.next_turn)

        self.current_tile = []  # [x, y]
        self.current_figure = []  # [x, y]
        self.current_turn = 1  # 1 - White, 0 - Black

    def onItemSelected(self):
        selected_item = self.sender().selectedItems()
        if selected_item:
            item = selected_item[0]
            row = item.row()
            col = item.column()
            self.current_tile = [row, col]
            # print(f"Выбрана ячейка в строке {row + 1}, столбце {col + 1}")
            if self.ui.field.item(row, col).background().color() == QColor(240, 240, 0):  # free cell move
                # print("Тут возможно будет ход!")
                pass
            elif self.ui.field.item(row, col).background().color() == QColor(240, 80, 0):  # attack move
                pass
                # print("Возможно тут будет труп!")
            elif field[row][col]:  # show figure possible moves
                self.current_figure = [row, col]
                if type(field[row][col]) == Pawn:
                    cells = pawn_moves(row, col)
                if type(field[row][col]) == Rook:
                    cells = rook_moves(row, col)
                if type(field[row][col]) == Bishop:
                    cells = bishop_moves(row, col)
                if type(field[row][col]) == Knight:
                    cells = knight_moves(row, col)
                if type(field[row][col]) == Queen:
                    cells = queen_moves(row, col)
                show_possible_items(cells, self.ui.field, field[row][col].color)
            else:
                self.current_figure = []
                update_cells(field, self.ui.field)
            # print("tile:", self.current_tile, "figure:", self.current_figure)

    def next_turn(self):
        if len(self.current_figure) == 2:  # if selected figure
            if self.current_figure != self.current_tile:  # and tile not the same
                x, y = self.current_tile[0], self.current_tile[1]
                x0, y0 = self.current_figure[0], self.current_figure[1]
                field[x][y] = field[x0][y0]
                field[x][y].move(x, y)  # updates coordinates
                field[x0][y0] = 0

                if type(field[x][y]) == Pawn:
                    field[x][y].first_move = False
        self.current_figure = []
        self.current_tile = []
        self.ui.field.clearSelection()
        update_cells(field, self.ui.field)

        if self.current_turn == 0:
            self.current_turn = 1
            self.ui.turn_label.setText("Ходят:\n\nБелые")
        else:
            self.current_turn = 0
            self.ui.turn_label.setText("Ходят:\n\nЧерные")


def pawn_moves(x, y):
    """
    Function returns list of all possible pawn moves [[x1, y1], [x2, y2], ...]

    :param x: figure x coordinate
    :param y: figure y coordinate
    :return: list
    """
    figure = field[x][y]
    c = [1, 2]
    res = []
    if x == 0 or x == 7:  # TODO: если пешка превратится на краю в крутыша
        return []
    if figure.color == 0:  # if black - moving down
        c = [-1, -2]  # coefficients to move up or down
    if not(field[x - c[0]][y]):  # if next upper cell isn't blocked
        res.append([x - c[0], y])
        if figure.first_move:
            if not(field[x - c[1]][y]):  # if cell through one isn't blocked
                res.append([x - c[1], y])
    if y != 0:  # not on left corner
        t = field[x - c[0]][y - 1]
        if t:  # if left diagonal cell has figure
            if t.color != figure.color:
                res.append([x - c[0], y - 1])  # possible attack cell
    if y != 7:  # not on right corner
        t = field[x - c[0]][y + 1]
        if t:  # if right diagonal cell has figure
            if t.color != figure.color:
                res.append([x - c[0], y + 1])  # possible attack cell
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
            if not(0 <= x - i <= 7 and 0 <= y - i <= 7):
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
    res1 = rook_moves(x, y)
    res2 = bishop_moves(x, y)
    return res1 + res2


def show_possible_items(cells, table, color):
    update_cells(field, table)
    for cell in cells:
        check_cell = field[cell[0]][cell[1]]
        if check_cell:  # If figure in cell
            if check_cell.color == color:  # and same color
                continue  # No move
            else:  # possible attack move
                create_figure(cell[0], cell[1], table, check_cell.image, QColor(240, 80, 0))
        else:  # free cell move
            create_figure(cell[0], cell[1], table, QPixmap, QColor(240, 240, 0))


def update_cells(matrix, table):
    for x, row in enumerate(matrix):
        for y, item in enumerate(row):
            if item:
                create_figure(x, y, table, item.image, default_color(x, y))
            else:
                create_figure(x, y, table, QPixmap, default_color(x, y))


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


def start_positions(table):
    # White figures:
    for i in range(8):
        create_figure(6, i, table, white_pawn_pixmap, default_color(6, i))
    create_figure(7, 0, table, white_rook_pixmap, default_color(7, 0))
    create_figure(7, 7, table, white_rook_pixmap, default_color(7, 7))
    create_figure(7, 1, table, white_knight_pixmap, default_color(7, 1))
    create_figure(7, 6, table, white_knight_pixmap, default_color(7, 6))
    create_figure(7, 2, table, white_bishop_pixmap, default_color(7, 2))
    create_figure(7, 5, table, white_bishop_pixmap, default_color(7, 5))
    create_figure(7, 3, table, white_queen_pixmap, default_color(7, 3))
    # Black figures:
    for i in range(8):
        create_figure(1, i, table, pawn_pixmap, default_color(1, i))
    create_figure(0, 0, table, rook_pixmap, default_color(0, 0))
    create_figure(0, 7, table, rook_pixmap, default_color(0, 7))
    create_figure(0, 1, table, knight_pixmap, default_color(0, 1))
    create_figure(0, 6, table, knight_pixmap, default_color(0, 6))
    create_figure(0, 2, table, bishop_pixmap, default_color(0, 2))
    create_figure(0, 5, table, bishop_pixmap, default_color(0, 5))
    create_figure(0, 3, table, queen_pixmap, default_color(0, 3))


def init_field_matrix(field):
    # White figures:
    for x in range(8):
        field[6][x] = Pawn(x, 6, color=1, image=white_pawn_pixmap)
    field[7][0] = Rook(7, 0, color=1, image=white_rook_pixmap)
    field[7][7] = Rook(7, 7, color=1, image=white_rook_pixmap)
    field[7][1] = Knight(7, 1, color=1, image=white_knight_pixmap)
    field[7][6] = Knight(7, 6, color=1, image=white_knight_pixmap)
    field[7][2] = Bishop(7, 2, color=1, image=white_bishop_pixmap)
    field[7][5] = Bishop(7, 5, color=1, image=white_bishop_pixmap)
    field[7][3] = Queen(7, 3, color=1, image=white_queen_pixmap)
    # Black figures:
    for x in range(8):
        field[1][x] = Pawn(x, 1, color=0, image=pawn_pixmap)
    field[0][0] = Rook(0, 0, color=0, image=rook_pixmap)
    field[0][7] = Rook(0, 7, color=0, image=rook_pixmap)
    field[0][1] = Knight(0, 1, color=0, image=knight_pixmap)
    field[0][6] = Knight(0, 6, color=0, image=knight_pixmap)
    field[0][2] = Bishop(0, 2, color=0, image=bishop_pixmap)
    field[0][5] = Bishop(0, 5, color=0, image=bishop_pixmap)
    field[0][3] = Queen(0, 3, color=0, image=queen_pixmap)


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

    # Matrix with class objects
    field = [[0 for j in range(8)] for i in range(8)]
    init_field_matrix(field)
    start_positions(window.ui.field)


    # DEBUG only
    # for row in field:
    #     print(row)

    window.show()
    sys.exit(app.exec())
