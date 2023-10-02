import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QVBoxLayout, QLabel
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

    def onItemSelected(self):
        selected_items = self.sender().selectedItems()
        if selected_items:
            for item in selected_items:
                row = item.row()
                col = item.column()
                print(f"Выбрана ячейка в строке {row}, столбце {col}")


def create_cell(x, y, color, table):
    item = QTableWidgetItem()
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    brush = QBrush(QColor(255, 255, 255))
    if color == 1:
        brush = QBrush(QColor(0, 0, 0))
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    item.setBackground(brush)
    table.field.setItem(x, y, item)


def create_figure(x, y, image, table):
    """
    Creates figure

    :param x: coordinate from 0 to 7
    :param y: coordinate from 0 to 7
    :param images: black or white Qpixmap
    :param table: window.ui.field
    :return: None
    """
    item = QTableWidgetItem()
    item.setData(Qt.ItemDataRole.DecorationRole, image)
    item.setBackground(QColor(0, 0, 0))
    if (x + y) % 2 != 1:
        item.setBackground(QColor(255, 255, 255))
    table.setItem(x, y, item)


def start_positions(table):
    create_figure(6, 0, white_pawn_pixmap, table)
    create_figure(6, 1, white_pawn_pixmap, table)
    create_figure(6, 2, white_pawn_pixmap, table)
    create_figure(6, 3, white_pawn_pixmap, table)
    create_figure(6, 4, white_pawn_pixmap, table)
    create_figure(6, 5, white_pawn_pixmap, table)
    create_figure(6, 6, white_pawn_pixmap, table)
    create_figure(6, 7, white_pawn_pixmap, table)

    create_figure(1, 0, pawn_pixmap, table)
    create_figure(1, 1, pawn_pixmap, table)
    create_figure(1, 2, pawn_pixmap, table)
    create_figure(1, 3, pawn_pixmap, table)
    create_figure(1, 4, pawn_pixmap, table)
    create_figure(1, 5, pawn_pixmap, table)
    create_figure(1, 6, pawn_pixmap, table)
    create_figure(1, 7, pawn_pixmap, table)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    figure_size = QSize(63, 63)

    pawn_pixmap = QPixmap(str(Path("src/pawn.png")))
    pawn_pixmap = pawn_pixmap.scaled(figure_size)  # , Qt.AspectRatioMode.KeepAspectRatio
    white_pawn_pixmap = QPixmap(str(Path("src/white_pawn.png")))
    white_pawn_pixmap = white_pawn_pixmap.scaled(figure_size)

    p1 = Pawn(6, 6, 1)

    start_positions(window.ui.field)

    window.show()
    sys.exit(app.exec())
