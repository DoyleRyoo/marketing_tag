from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.loadedSettings = {
            ("내용 설정", "소량제작"): "",
            ("내용 설정", "맞춤제작"): "",
            ("플랫폼 설정", "소량제작"): "",
            ("플랫폼 설정", "맞춤제작"): "",
        }
        self.isDirty = False

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(24, 24, 24, 24)
        mainLayout.setSpacing(18)

        titleLabel = QLabel("설정")
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(self._createCategoryLayout())
        mainLayout.addLayout(self._createTemplateLayout())
        mainLayout.addWidget(self._createEditorArea(), 1)
        mainLayout.addLayout(self._createBottomLayout())

        self._loadCurrentSettingsToEditor()
        self._setDirtyState(False)

    def _createCategoryLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.contentSettingsButton = QPushButton("내용 설정")
        self.platformSettingsButton = QPushButton("플랫폼 설정")
        self.contentSettingsButton.setCheckable(True)
        self.platformSettingsButton.setCheckable(True)
        self.contentSettingsButton.setChecked(True)

        categoryButtonGroup = QButtonGroup(self)
        categoryButtonGroup.setExclusive(True)
        categoryButtonGroup.addButton(self.contentSettingsButton)
        categoryButtonGroup.addButton(self.platformSettingsButton)

        self.contentSettingsButton.clicked.connect(self._handleSelectionChanged)
        self.platformSettingsButton.clicked.connect(self._handleSelectionChanged)

        layout.addWidget(self.contentSettingsButton)
        layout.addWidget(self.platformSettingsButton)
        layout.addStretch(1)

        return layout

    def _createTemplateLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.smallQuantityTemplateButton = QPushButton("소량제작")
        self.customTemplateButton = QPushButton("맞춤제작")
        self.smallQuantityTemplateButton.setCheckable(True)
        self.customTemplateButton.setCheckable(True)
        self.smallQuantityTemplateButton.setChecked(True)

        templateButtonGroup = QButtonGroup(self)
        templateButtonGroup.setExclusive(True)
        templateButtonGroup.addButton(self.smallQuantityTemplateButton)
        templateButtonGroup.addButton(self.customTemplateButton)

        self.smallQuantityTemplateButton.clicked.connect(self._handleSelectionChanged)
        self.customTemplateButton.clicked.connect(self._handleSelectionChanged)

        layout.addWidget(self.smallQuantityTemplateButton)
        layout.addWidget(self.customTemplateButton)
        layout.addStretch(1)

        return layout

    def _createEditorArea(self) -> QFrame:
        self.editorFrame = QFrame()
        self.editorFrame.setFrameShape(QFrame.Shape.StyledPanel)

        editorLayout = QVBoxLayout(self.editorFrame)
        self.editorTitleLabel = QLabel()
        self.settingsEdit = QPlainTextEdit()
        self.settingsEdit.setPlaceholderText("설정 편집")
        self.settingsEdit.textChanged.connect(self._handleSettingsEdited)

        editorLayout.addWidget(self.editorTitleLabel)
        editorLayout.addWidget(self.settingsEdit, 1)

        return self.editorFrame

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

    def _currentCategoryText(self) -> str:
        if self.contentSettingsButton.isChecked():
            return self.contentSettingsButton.text()
        return self.platformSettingsButton.text()

    def _currentTemplateText(self) -> str:
        if self.smallQuantityTemplateButton.isChecked():
            return self.smallQuantityTemplateButton.text()
        return self.customTemplateButton.text()

    def _currentSettingsKey(self) -> tuple[str, str]:
        return (self._currentCategoryText(), self._currentTemplateText())

    def _updateEditorTitle(self) -> None:
        self.editorTitleLabel.setText(
            f"{self._currentCategoryText()} / {self._currentTemplateText()}"
        )

    def _loadCurrentSettingsToEditor(self) -> None:
        self._updateEditorTitle()
        self.settingsEdit.blockSignals(True)
        self.settingsEdit.setPlainText(self.loadedSettings[self._currentSettingsKey()])
        self.settingsEdit.blockSignals(False)

    def _setDirtyState(self, isDirty: bool) -> None:
        self.isDirty = isDirty
        self.dirtyStateLabel.setVisible(isDirty)
        self.cancelButton.setEnabled(isDirty)
        self.saveChangesButton.setEnabled(isDirty)

    def _handleSettingsEdited(self) -> None:
        self._setDirtyState(True)

    def _handleSelectionChanged(self) -> None:
        self._loadCurrentSettingsToEditor()
        self._setDirtyState(False)

    def _handleCancelClicked(self) -> None:
        self._loadCurrentSettingsToEditor()
        self._setDirtyState(False)

    def _handleSaveClicked(self) -> None:
        self.loadedSettings[self._currentSettingsKey()] = self.settingsEdit.toPlainText()
        self._setDirtyState(False)

    def _handleRestoreDefaultsClicked(self) -> None:
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Icon.Question)
        messageBox.setWindowTitle("기본값 복원")
        messageBox.setText(
            f"현재 선택된 템플릿({self._currentTemplateText()})의 기본값을 복원하시겠습니까?"
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
