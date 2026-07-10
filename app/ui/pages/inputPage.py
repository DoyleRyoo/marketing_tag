from pathlib import Path

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


class InputPage(QWidget):
    MAX_IMAGE_COUNT = 9

    def __init__(self) -> None:
        super().__init__()

        self.thumbnailFilePath = ""

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(24, 24, 24, 24)
        mainLayout.setSpacing(18)

        titleLabel = QLabel("입력")
        mainLayout.addWidget(titleLabel)

        mainLayout.addLayout(self._createTemplateLayout())
        mainLayout.addLayout(self._createThumbnailLayout())
        mainLayout.addLayout(self._createImageLayout())
        mainLayout.addLayout(self._createContentLayout(), 1)
        mainLayout.addLayout(self._createBottomButtonLayout())

    def setThumbnailPreview(self, filePath: str) -> None:
        path = Path(filePath)
        self.thumbnailFilePath = filePath

        self.thumbnailPreviewLabel.setText(str(path))
        self.thumbnailFileNameLabel.setText(path.name)
        self.thumbnailSelectButton.setEnabled(False)
        self.thumbnailChangeButton.setEnabled(True)
        self.thumbnailDeleteButton.setEnabled(True)

    def clearThumbnailPreview(self) -> None:
        self.thumbnailFilePath = ""
        self.thumbnailPreviewLabel.setText("선택된 이미지 없음")
        self.thumbnailFileNameLabel.clear()
        self.thumbnailSelectButton.setEnabled(True)
        self.thumbnailChangeButton.setEnabled(False)
        self.thumbnailDeleteButton.setEnabled(False)

    def addImageItem(self, filePath: str) -> None:
        if len(self.imageItemWidgets) >= self.MAX_IMAGE_COUNT:
            return

        path = Path(filePath)
        itemWidget = QWidget()
        itemLayout = QHBoxLayout(itemWidget)
        itemLayout.setContentsMargins(0, 0, 0, 0)

        fileNameLabel = QLabel(path.name)
        deleteButton = QPushButton("삭제")

        itemLayout.addWidget(fileNameLabel, 1)
        itemLayout.addWidget(deleteButton)

        deleteButton.clicked.connect(
            lambda checked=False, widget=itemWidget: self._removeImageItemWidget(widget)
        )

        self.imageItemWidgets.append(itemWidget)
        self.emptyImageLabel.setVisible(False)
        self.imageListLayout.insertWidget(self.imageListLayout.count() - 1, itemWidget)
        self.updateImageCount()

    def removeImageItem(self, index: int) -> None:
        if index < 0 or index >= len(self.imageItemWidgets):
            return

        itemWidget = self.imageItemWidgets.pop(index)
        self.imageListLayout.removeWidget(itemWidget)
        itemWidget.deleteLater()

        self.emptyImageLabel.setVisible(len(self.imageItemWidgets) == 0)
        self.updateImageCount()

    def clearImageItems(self) -> None:
        while self.imageItemWidgets:
            self.removeImageItem(0)

    def updateImageCount(self) -> None:
        self.imageCountLabel.setText(f"{len(self.imageItemWidgets)} / {self.MAX_IMAGE_COUNT}장")

    def resetInputs(self) -> None:
        self.contentEdit.clear()
        self.clearThumbnailPreview()
        self.clearImageItems()

    def _removeImageItemWidget(self, itemWidget: QWidget) -> None:
        if itemWidget in self.imageItemWidgets:
            self.removeImageItem(self.imageItemWidgets.index(itemWidget))

    def _handleResetClicked(self) -> None:
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Icon.Question)
        messageBox.setWindowTitle("초기화")
        messageBox.setText("입력한 내용을 모두 초기화하시겠습니까?")

        cancelButton = messageBox.addButton("취소", QMessageBox.ButtonRole.RejectRole)
        resetButton = messageBox.addButton("초기화", QMessageBox.ButtonRole.AcceptRole)
        messageBox.setDefaultButton(cancelButton)
        messageBox.exec()

        if messageBox.clickedButton() == resetButton:
            self.resetInputs()

    def _handleGenerateClicked(self) -> None:
        if not self.contentEdit.toPlainText():
            QMessageBox.warning(self, "필수 입력", "내용을 입력하세요.")
            return

        if not self.thumbnailFilePath:
            QMessageBox.warning(self, "필수 입력", "썸네일 이미지를 선택하세요.")
            return

        mainWindow = self.window()
        if hasattr(mainWindow, "showOutputPage"):
            mainWindow.showOutputPage()

    def _createTemplateLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        label = QLabel("템플릿")
        smallQuantityButton = QPushButton("소량제작")
        customButton = QPushButton("맞춤제작")

        smallQuantityButton.setCheckable(True)
        customButton.setCheckable(True)
        smallQuantityButton.setChecked(True)

        templateButtonGroup = QButtonGroup(self)
        templateButtonGroup.setExclusive(True)
        templateButtonGroup.addButton(smallQuantityButton)
        templateButtonGroup.addButton(customButton)

        layout.addWidget(label)
        layout.addWidget(smallQuantityButton)
        layout.addWidget(customButton)
        layout.addStretch(1)

        return layout

    def _createThumbnailLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.thumbnailPreviewLabel = QLabel("선택된 이미지 없음")
        self.thumbnailPreviewLabel.setFrameShape(QFrame.Shape.StyledPanel)
        self.thumbnailPreviewLabel.setMinimumSize(180, 100)

        self.thumbnailFileNameLabel = QLabel()
        self.thumbnailSelectButton = QPushButton("파일 선택")
        self.thumbnailChangeButton = QPushButton("변경")
        self.thumbnailDeleteButton = QPushButton("삭제")

        self.thumbnailChangeButton.setEnabled(False)
        self.thumbnailDeleteButton.setEnabled(False)

        layout.addWidget(QLabel("썸네일"))
        layout.addWidget(self.thumbnailPreviewLabel)
        layout.addWidget(self.thumbnailFileNameLabel, 1)
        layout.addWidget(self.thumbnailSelectButton)
        layout.addWidget(self.thumbnailChangeButton)
        layout.addWidget(self.thumbnailDeleteButton)

        return layout

    def _createImageLayout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        headerLayout = QHBoxLayout()
        self.imageAddButton = QPushButton("이미지 추가")
        self.imageCountLabel = QLabel()

        headerLayout.addWidget(QLabel("일반 이미지"))
        headerLayout.addWidget(self.imageAddButton)
        headerLayout.addStretch(1)
        headerLayout.addWidget(self.imageCountLabel)

        imageListFrame = QFrame()
        imageListFrame.setFrameShape(QFrame.Shape.StyledPanel)
        imageListFrame.setMinimumHeight(120)

        self.imageItemWidgets: list[QWidget] = []
        self.imageListLayout = QVBoxLayout(imageListFrame)
        self.emptyImageLabel = QLabel("추가된 이미지 없음")
        self.imageListLayout.addWidget(self.emptyImageLabel)
        self.imageListLayout.addStretch(1)

        layout.addLayout(headerLayout)
        layout.addWidget(imageListFrame)

        self.updateImageCount()

        return layout

    def _createContentLayout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        layout.addWidget(QLabel("내용"))
        self.contentEdit = QPlainTextEdit()
        self.contentEdit.setPlaceholderText(
            "기업 : 시너진\n"
            "품명 : 생분해 지퍼백\n"
            "규격 : 320*430+20\n"
            "소재 : EL724(생분해)\n"
            "인쇄 :단면_1도 블랙\n"
            "링크:https://www.example.com/"
        )
        layout.addWidget(self.contentEdit, 1)

        return layout

    def _createBottomButtonLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.resetButton = QPushButton("초기화")
        self.generateButton = QPushButton("HTML 생성")
        self.resetButton.clicked.connect(self._handleResetClicked)
        self.generateButton.clicked.connect(self._handleGenerateClicked)

        layout.addStretch(1)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.generateButton)

        return layout
