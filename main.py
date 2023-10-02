import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from generated_ui import Ui_Dialog  # Импортируйте сгенерированный модуль


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создайте экземпляр класса Ui_MainWindow и настройте UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
