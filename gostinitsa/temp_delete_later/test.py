import psycopg2
import sys
from PyQt6 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример closeEvent")
        
    def closeEvent(self, event: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Выход",
            "Вы уверены, что хотите выйти?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            print("Завершаем ресурсы, например, закрываем подключение...")
            event.accept()  # Подтверждаем закрытие
        else:
            event.ignore()  # Отклоняем закрытие

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())