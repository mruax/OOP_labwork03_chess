import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from generated_ui import Ui_Dialog
from chess import Pawn


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

    def onItemSelected(self):
        selected_item = self.sender().selectedItems()
        if selected_item:
            item = selected_item[0]
            row = item.row()
            col = item.column()
            print(f"Выбрана ячейка в строке {row + 1}, столбце {col + 1}")
            if self.ui.field.item(row, col).background().color() == QColor(240, 240, 0):  # free cell move
                print("Тут возможно будет ход!")
            elif self.ui.field.item(row, col).background().color() == QColor(240, 80, 0):  # attack move
                print("Возможно тут будет труп!")
            elif field[row][col]:  # show figure possible moves
                # cells = field[row][col].possible_moves()
                cells = pawn_moves(row, col)
                print("Возможные ходы:", cells)
                show_possible_items(cells, self.ui.field, field[row][col].color)
            else:
                update_cells(field, self.ui.field)

    def next_turn(self):
        print("Новый ход!")


def pawn_moves(x, y):
    figure = field[x][y]
    c = [1, 2]
    res = []
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
    for i in range(8):
        create_figure(6, i, table, white_pawn_pixmap, default_color(6, i))
    for i in range(8):
        create_figure(1, i, table, pawn_pixmap, default_color(1, i))


def init_field_matrix(field):
    # Black figures:
    for x in range(8):
        field[1][x] = Pawn(x, 1, color=0, image=pawn_pixmap)
    # White figures:
    for x in range(8):
        field[6][x] = Pawn(x, 6, color=1, image=white_pawn_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    figure_size = QSize(63, 63)
    pawn_pixmap = QPixmap(str(Path("src/pawn.png")))
    pawn_pixmap = pawn_pixmap.scaled(figure_size)  # , Qt.AspectRatioMode.KeepAspectRatio
    white_pawn_pixmap = QPixmap(str(Path("src/white_pawn.png")))
    white_pawn_pixmap = white_pawn_pixmap.scaled(figure_size)

    field = [[0 for j in range(8)] for i in range(8)]
    init_field_matrix(field)
    for row in field:
        print(row)
    start_positions(window.ui.field)

    # test figures:
    field[5][3] = Pawn(3, 5, color=1, image=white_pawn_pixmap)
    create_figure(5, 3, window.ui.field, white_pawn_pixmap, default_color(3, 5))
    field[4][2] = Pawn(2, 4, color=0, image=pawn_pixmap)
    create_figure(4, 2, window.ui.field, pawn_pixmap, default_color(2, 4))
    field[4][4] = Pawn(4, 4, color=0, image=pawn_pixmap)
    create_figure(4, 4, window.ui.field, pawn_pixmap, default_color(4, 4))

    current_turn = 1  # 1 - White, 0 - Black

    # table.clearSelection()
    window.show()
    sys.exit(app.exec())
