from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.ui.pages.inputPage import InputPage
from app.ui.pages.outputPage import OutputPage
from app.ui.pages.settingsPage import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("칼렛스토어 HTML 매크로")
        self.resize(1200, 850)

        self.stackedWidget = QStackedWidget()
        self.inputPage = InputPage()
        self.outputPage = OutputPage()
        self.settingsPage = SettingsPage()

        self.stackedWidget.addWidget(self.inputPage)
        self.stackedWidget.addWidget(self.outputPage)
        self.stackedWidget.addWidget(self.settingsPage)

        self.setCentralWidget(self.stackedWidget)
        self.showInputPage()

    def showInputPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.inputPage)

    def showOutputPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.outputPage)

    def showSettingsPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.settingsPage)
