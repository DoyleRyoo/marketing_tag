from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class SettingsPage(QWidget):
    TEMPLATE_OPTIONS = (
        ("smallQuantityTemplate", "소량제작"),
        ("customTemplate", "맞춤제작"),
    )
    CATEGORY_OPTIONS = (
        ("content", "내용 설정"),
        ("naver", "네이버 설정"),
        ("wordpress", "워드프레스 설정"),
        ("companyMall", "자사몰 설정"),
    )

    def __init__(self) -> None:
        super().__init__()

        self.loadedSettings = {
            (templateKey, categoryKey): ""
            for templateKey, _ in self.TEMPLATE_OPTIONS
            for categoryKey, _ in self.CATEGORY_OPTIONS
        }
        self.editorPages: dict[tuple[str, str], QPlainTextEdit] = {}
        self.isDirty = False

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(24, 24, 24, 24)
        mainLayout.setSpacing(18)

        titleLabel = QLabel("설정")
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(self._createTemplateLayout())
        mainLayout.addLayout(self._createCategoryLayout())
        mainLayout.addWidget(self._createEditorArea(), 1)
        mainLayout.addLayout(self._createBottomLayout())

        self._applyCurrentSelectionToUi()
        self._setDirtyState(False)

    def _createTemplateLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.templateButtons: dict[str, QPushButton] = {}
        self.templateButtonGroup = QButtonGroup(self)
        self.templateButtonGroup.setExclusive(True)

        for index, (templateKey, labelText) in enumerate(self.TEMPLATE_OPTIONS):
            button = QPushButton(labelText)
            button.setCheckable(True)
            button.clicked.connect(self._handleSelectionChanged)
            self.templateButtonGroup.addButton(button)
            self.templateButtons[templateKey] = button
            layout.addWidget(button)

            if index == 0:
                button.setChecked(True)

        layout.addStretch(1)

        return layout

    def _createCategoryLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.categoryButtons: dict[str, QPushButton] = {}
        self.categoryButtonGroup = QButtonGroup(self)
        self.categoryButtonGroup.setExclusive(True)

        for index, (categoryKey, labelText) in enumerate(self.CATEGORY_OPTIONS):
            button = QPushButton(labelText)
            button.setCheckable(True)
            button.clicked.connect(self._handleSelectionChanged)
            self.categoryButtonGroup.addButton(button)
            self.categoryButtons[categoryKey] = button
            layout.addWidget(button)

            if index == 0:
                button.setChecked(True)

        layout.addStretch(1)

        return layout

    def _createEditorArea(self) -> QFrame:
        self.editorFrame = QFrame()
        self.editorFrame.setFrameShape(QFrame.Shape.StyledPanel)

        editorLayout = QVBoxLayout(self.editorFrame)
        self.editorTitleLabel = QLabel()
        self.editorStack = QStackedWidget()

        editorLayout.addWidget(self.editorTitleLabel)
        editorLayout.addWidget(self.editorStack, 1)

        for templateKey, templateLabel in self.TEMPLATE_OPTIONS:
            for categoryKey, categoryLabel in self.CATEGORY_OPTIONS:
                page = self._createEditorPage(templateLabel, categoryLabel)
                self.editorPages[(templateKey, categoryKey)] = page
                self.editorStack.addWidget(page)

        return self.editorFrame

    def _createEditorPage(
        self, templateLabel: str, categoryLabel: str
    ) -> QPlainTextEdit:
        editor = QPlainTextEdit()
        editor.setPlaceholderText(f"{templateLabel} / {categoryLabel}")
        editor.textChanged.connect(self._handleSettingsEdited)

        return editor

    def _createBottomLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.dirtyStateLabel = QLabel("저장되지 않은 변경사항이 있습니다.")
        self.dirtyStateLabel.setVisible(False)

        self.restoreDefaultsButton = QPushButton("기본값 복원")
        self.cancelButton = QPushButton("취소")
        self.saveChangesButton = QPushButton("변경사항 저장")
        self.cancelButton.setEnabled(False)
        self.saveChangesButton.setEnabled(False)

        self.restoreDefaultsButton.clicked.connect(self._handleRestoreDefaultsClicked)
        self.cancelButton.clicked.connect(self._handleCancelClicked)
        self.saveChangesButton.clicked.connect(self._handleSaveClicked)

        layout.addWidget(self.dirtyStateLabel)
        layout.addStretch(1)
        layout.addWidget(self.restoreDefaultsButton)
        layout.addWidget(self.cancelButton)
        layout.addWidget(self.saveChangesButton)

        return layout

    def getCurrentTemplateKey(self) -> str:
        for templateKey, button in self.templateButtons.items():
            if button.isChecked():
                return templateKey

        return self.TEMPLATE_OPTIONS[0][0]

    def getCurrentCategoryKey(self) -> str:
        for categoryKey, button in self.categoryButtons.items():
            if button.isChecked():
                return categoryKey

        return self.CATEGORY_OPTIONS[0][0]

    def _currentSettingsKey(self) -> tuple[str, str]:
        return (self.getCurrentTemplateKey(), self.getCurrentCategoryKey())

    def _currentTemplateLabel(self) -> str:
        return self.templateButtons[self.getCurrentTemplateKey()].text()

    def _currentCategoryLabel(self) -> str:
        return self.categoryButtons[self.getCurrentCategoryKey()].text()

    def _currentEditor(self) -> QPlainTextEdit:
        return self.editorPages[self._currentSettingsKey()]

    def _applyCurrentSelectionToUi(self) -> None:
        currentEditor = self._currentEditor()
        self.editorStack.setCurrentWidget(currentEditor)
        self.editorTitleLabel.setText(
            f"{self._currentTemplateLabel()} / {self._currentCategoryLabel()}"
        )

        currentEditor.blockSignals(True)
        currentEditor.setPlainText(self.loadedSettings[self._currentSettingsKey()])
        currentEditor.blockSignals(False)

    def _setDirtyState(self, isDirty: bool) -> None:
        self.isDirty = isDirty
        self.dirtyStateLabel.setVisible(isDirty)
        self.cancelButton.setEnabled(isDirty)
        self.saveChangesButton.setEnabled(isDirty)

    def _handleSettingsEdited(self) -> None:
        self._setDirtyState(True)

    def _handleSelectionChanged(self) -> None:
        self._applyCurrentSelectionToUi()
        self._setDirtyState(False)

    def _handleCancelClicked(self) -> None:
        self._applyCurrentSelectionToUi()
        self._setDirtyState(False)

    def _handleSaveClicked(self) -> None:
        self.loadedSettings[self._currentSettingsKey()] = (
            self._currentEditor().toPlainText()
        )
        self._setDirtyState(False)

    def _handleRestoreDefaultsClicked(self) -> None:
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Icon.Question)
        messageBox.setWindowTitle("기본값 복원")
        messageBox.setText(
            f"현재 선택된 템플릿({self._currentTemplateLabel()})의 기본값을 복원하시겠습니까?"
        )

        cancelButton = messageBox.addButton("취소", QMessageBox.ButtonRole.RejectRole)
        restoreButton = messageBox.addButton(
            "기본값 복원", QMessageBox.ButtonRole.AcceptRole
        )
        messageBox.setDefaultButton(cancelButton)
        messageBox.exec()

        if messageBox.clickedButton() == restoreButton:
            self._restoreCurrentTemplateDefaults()

    def _restoreCurrentTemplateDefaults(self) -> None:
        self._setDirtyState(True)
