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

        # manually added fixed restriction
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
            if field[row][col]:
                cells = field[row][col].possible_moves()
                print("Возможные ходы:", cells)
                show_possible_items(cells, self.ui.field)
            else:
                update_cells(field, self.ui.field)

    def next_turn(self):
        print("Новый ход!")


def show_possible_items(cells, table):
    update_cells(field, table)
    for cell in cells:
        # create_figure(cell[0], cell[1], table, QColor(200, 200, 0), pawn_pixmap)
        # table.clearSelection()
        create_figure(cell[1], cell[0], table, QPixmap, QColor(240, 240, 0))


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

    current_turn = 1  # 1 - White, 0 - Black


    window.show()
    sys.exit(app.exec())
