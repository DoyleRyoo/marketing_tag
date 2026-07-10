from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class OutputPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.platformResults = {
            "네이버": "",
            "워드프레스": "",
            "칼렛스토어": "",
        }

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(24, 24, 24, 24)
        mainLayout.setSpacing(18)

        titleLabel = QLabel("출력")
        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self._createPlatformTabs())
        mainLayout.addLayout(self._createViewModeLayout())
        mainLayout.addWidget(self._createResultArea(), 1)
        mainLayout.addWidget(QLabel("현재 작업은 자동 저장되지 않습니다."))
        mainLayout.addLayout(self._createBottomButtonLayout())

        self._updateResultDisplay()
        self.updateOutputButtonState()

    def setPlatformHtml(self, platform: str, html: str) -> None:
        if platform not in self.platformResults:
            return

        self.platformResults[platform] = html
        if platform == self._currentPlatformName():
            self._updateResultDisplay()
            self.updateOutputButtonState()

    def getCurrentPlatformHtml(self) -> str:
        return self.platformResults[self._currentPlatformName()]

    def updateOutputButtonState(self) -> None:
        hasHtml = bool(self.getCurrentPlatformHtml())
        self.copyCodeButton.setEnabled(hasHtml)
        self.saveFileButton.setEnabled(hasHtml)

    def _createPlatformTabs(self) -> QTabWidget:
        self.platformTabs = QTabWidget()
        self.platformTabs.addTab(QWidget(), "네이버")
        self.platformTabs.addTab(QWidget(), "워드프레스")
        self.platformTabs.addTab(QWidget(), "칼렛스토어")
        self.platformTabs.currentChanged.connect(self._handlePlatformChanged)

        return self.platformTabs

    def _createViewModeLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.previewButton = QPushButton("미리보기")
        self.htmlCodeButton = QPushButton("HTML 코드")
        self.previewButton.setCheckable(True)
        self.htmlCodeButton.setCheckable(True)
        self.previewButton.setChecked(True)

        viewModeButtonGroup = QButtonGroup(self)
        viewModeButtonGroup.setExclusive(True)
        viewModeButtonGroup.addButton(self.previewButton)
        viewModeButtonGroup.addButton(self.htmlCodeButton)

        self.previewButton.clicked.connect(self._showPreview)
        self.htmlCodeButton.clicked.connect(self._showHtmlCode)

        layout.addStretch(1)
        layout.addWidget(self.previewButton)
        layout.addWidget(self.htmlCodeButton)

        return layout

    def _createResultArea(self) -> QFrame:
        self.resultFrame = QFrame()
        self.resultFrame.setFrameShape(QFrame.Shape.StyledPanel)

        resultLayout = QVBoxLayout(self.resultFrame)
        self.resultStack = QStackedWidget()

        self.previewContainer = QWidget()
        previewLayout = QVBoxLayout(self.previewContainer)
        self.previewLabel = QLabel()
        self.previewLabel.setWordWrap(True)
        previewLayout.addWidget(self.previewLabel)
        previewLayout.addStretch(1)

        self.htmlCodeEdit = QPlainTextEdit()
        self.htmlCodeEdit.setReadOnly(True)

        self.resultStack.addWidget(self.previewContainer)
        self.resultStack.addWidget(self.htmlCodeEdit)

        resultLayout.addWidget(self.resultStack)

        return self.resultFrame

    def _createBottomButtonLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.backToInputButton = QPushButton("입력으로 돌아가기")
        self.copyCodeButton = QPushButton("코드 복사")
        self.saveFileButton = QPushButton("파일 저장")
        self.backToInputButton.clicked.connect(self._handleBackToInputClicked)

        layout.addWidget(self.backToInputButton)
        layout.addStretch(1)
        layout.addWidget(self.copyCodeButton)
        layout.addWidget(self.saveFileButton)

        return layout

    def _handleBackToInputClicked(self) -> None:
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Icon.Question)
        messageBox.setWindowTitle("입력 화면으로 돌아가기")
        messageBox.setText(
            "입력 화면으로 돌아가시겠습니까?\n\n"
            "현재 작업은 파일에 자동 저장되지 않습니다.\n"
            "입력값은 프로그램이 실행되는 동안 유지되지만,\n"
            "프로그램을 종료하면 복구할 수 없습니다."
        )

        cancelButton = messageBox.addButton("취소", QMessageBox.ButtonRole.RejectRole)
        backButton = messageBox.addButton(
            "입력으로 돌아가기", QMessageBox.ButtonRole.AcceptRole
        )
        messageBox.setDefaultButton(cancelButton)
        messageBox.exec()

        if messageBox.clickedButton() == backButton:
            mainWindow = self.window()
            if hasattr(mainWindow, "showInputPage"):
                mainWindow.showInputPage()

    def _handlePlatformChanged(self) -> None:
        self._updateResultDisplay()
        self.updateOutputButtonState()

    def _currentPlatformName(self) -> str:
        return self.platformTabs.tabText(self.platformTabs.currentIndex())

    def _updateResultDisplay(self) -> None:
        currentHtml = self.getCurrentPlatformHtml()
        self.previewLabel.setText(currentHtml)
        self.htmlCodeEdit.setPlainText(currentHtml)

    def _showPreview(self) -> None:
        self.resultStack.setCurrentWidget(self.previewContainer)

    def _showHtmlCode(self) -> None:
        self.resultStack.setCurrentWidget(self.htmlCodeEdit)
