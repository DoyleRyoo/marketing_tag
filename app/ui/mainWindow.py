from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

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

        self.inputPage.settingsRequested.connect(self.showSettingsPage)

        self.stackedWidget.addWidget(self.inputPage)
        self.stackedWidget.addWidget(self.outputPage)
        self.stackedWidget.addWidget(self.settingsPage)

        self.setCentralWidget(self._createCentralWidget())
        self.showInputPage()

    def _createCentralWidget(self) -> QWidget:
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self._createDevelopmentNavigation())
        layout.addWidget(self.stackedWidget, 1)

        return centralWidget

    def _createDevelopmentNavigation(self) -> QWidget:
        # 임시 개발용 페이지 전환 메뉴입니다. 개발 완료 시 이 메서드 호출만 제거하면 됩니다.
        navigationWidget = QWidget()
        layout = QHBoxLayout(navigationWidget)

        inputButton = QPushButton("입력 화면")
        outputButton = QPushButton("출력 화면")
        settingsButton = QPushButton("설정 화면")

        inputButton.clicked.connect(self.showInputPage)
        outputButton.clicked.connect(self.showOutputPage)
        settingsButton.clicked.connect(self.showSettingsPage)

        layout.addWidget(QLabel("개발 화면 전환"))
        layout.addWidget(inputButton)
        layout.addWidget(outputButton)
        layout.addWidget(settingsButton)
        layout.addStretch(1)

        return navigationWidget

    def showInputPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.inputPage)

    def showOutputPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.outputPage)

    def showSettingsPage(self) -> None:
        self.stackedWidget.setCurrentWidget(self.settingsPage)
