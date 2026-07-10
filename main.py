import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("칼렛스토어 HTML 매크로")
        self.resize(1200, 800)

        label = QLabel("HTML 매크로 개발 환경이 정상적으로 실행되었습니다.")
        self.setCentralWidget(label)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())