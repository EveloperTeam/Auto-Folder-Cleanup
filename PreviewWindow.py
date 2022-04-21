import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class PreviewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sub Window')
        self.resize(1000, 1000)
        self.setStyleSheet("background-color:#E5E9F5;")
        self.center()

        #Layout 설정
        layout = QVBoxLayout()
        TitleLayout = QHBoxLayout()
        ButtonLayout = QHBoxLayout()
        PreviewLayout = QHBoxLayout()
        LeftGroupBox = QGroupBox('변경 전')
        RightGroupBox = QGroupBox('변경 후')


        #미리보기 아이콘 추가
        pixmap = QPixmap('./img/preview.png')

        previewImg = QLabel()
        previewImg.setPixmap(pixmap)

        #GroupBox 설정
        LeftGroupBox.setStyleSheet(
            'QGroupBox{'
                        'border-radius: 10px;'
                        'border: 2px solid;'
                        'margin-top: 40px;'
                        'background-color: #85B6FF;'
                        'font-size: 30px;'
                        'font-weight: bold;}'
            'QGroupBox:title {'
                         'border-top-left-radius: 3px;'
                         'border-top-right-radius: 3px;'
                         'subcontrol-origin: margin;'
                         'subcontrol-position: top center;'
                         'padding-left: 10px;'
                         'padding-right: 10px;}')

        RightGroupBox.setStyleSheet(
            'QGroupBox{'
                        'border-radius: 10px;'
                        'border: 2px solid;'
                        'margin-top: 40px;'
                        'background-color: #85B6FF;'
                        'font-size: 30px;'
                        'font-weight: bold;}'
            'QGroupBox:title {'
                         'subcontrol-origin: margin;'
                         'subcontrol-position: top center;'
                         'padding-left: 10px;'
                         'padding-right: 10px; }')

        #Label 설정
        titleLabel = QLabel('미리보기', self)
        titleLabel.setFixedHeight(50)
        warningLabel = QLabel('정리를 시작하면 되돌릴 수 없습니다. 이대로 진행하시겠습니까?', self)

        titleFont = titleLabel.font()
        titleFont.setPointSize(40)
        titleFont.setBold(True)

        warningFont = warningLabel.font()
        warningFont.setPointSize(30)
        warningFont.setBold(True)

        titleLabel.setFont(titleFont)
        warningLabel.setFont(warningFont)

        #Button 설정
        btnOK = QPushButton()
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnOK.setIcon(QIcon('./img/check.png'))
        btnOK.setStyleSheet("border-radius:15px; border:2px solid black; background-color:#00DC58; padding:20px;")

        btnCancel = QPushButton()
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        btnCancel.setIcon(QIcon('./img/close.png'))
        btnCancel.setStyleSheet("border-radius:15px; border:2px solid black; background-color:#FF0000; padding:20px;")


        #위젯 추가
        TitleLayout.addWidget(previewImg)
        TitleLayout.addWidget(titleLabel)
        TitleLayout.setAlignment(Qt.AlignLeft)

        PreviewLayout.addWidget(LeftGroupBox)
        PreviewLayout.addWidget(RightGroupBox)

        ButtonLayout.addWidget(warningLabel)
        ButtonLayout.addStretch(5)
        ButtonLayout.addWidget(btnOK)
        ButtonLayout.addWidget(btnCancel)

        layout.addLayout(TitleLayout)
        layout.addLayout(PreviewLayout)
        layout.addLayout(ButtonLayout)

        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())