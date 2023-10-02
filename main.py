import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from generated_ui import Ui_Dialog


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

        # for row in range(8):
        #     for col in range(8):
        #         item = QTableWidgetItem()
        #         item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        #         self.ui.field.setItem(row, col, item)

        self.ui.field.itemClicked.connect(self.onItemClicked)
        # self.ui.field.itemSelectionChanged.connect(self.onItemSelected)

    def onItemClicked(self, item):
        if item.isSelected():
            # Если да, снимаем выделение
            self.ui.field.clearSelection()
        else:
            # Если нет, выделяем ячейку
            item.setSelected(True)
        # selected_items = self.sender().selectedItems()
        # if selected_items:
        #     for item in selected_items:
        #         row = item.row()
        #         col = item.column()
        #         print(f"Выбрана ячейка в строке {row}, столбце {col}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
