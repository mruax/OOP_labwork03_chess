import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from chess import Pawn, Rook, Bishop, Knight, Queen, King
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

        self.ui.field.itemSelectionChanged.connect(self.onItemSelected)
        self.ui.turn_button.clicked.connect(self.next_turn)

    def onItemSelected(self):
        pass

    def next_turn(self):
        pass


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
    init_field_matrix(field)

    # Show figures on board
    start_positions(window.ui.field)


    window.show()
    sys.exit(app.exec())