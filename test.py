import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QRect, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Центрирование окна")
        self.resize(400, 300)  # Устанавливаем начальный размер окна

        # Центрируем окно
        self.center_window()

        # Простая метка внутри окна
        central_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Окно по центру экрана")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        # Получаем размеры экрана
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Получаем размеры окна
        window_geometry = self.frameGeometry()

        # Рассчитываем центральную точку экрана
        screen_center = screen_geometry.center()

        # Перемещаем окно так, чтобы оно было по центру экрана
        window_geometry.moveCenter(screen_center)

        # Устанавливаем новое положение окна
        self.move(window_geometry.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
