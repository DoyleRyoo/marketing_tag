from PySide6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("칼렛스토어 HTML 매크로")
        self.resize(1200, 850)
        self.setCentralWidget(QWidget())
