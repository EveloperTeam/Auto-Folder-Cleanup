from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ConfirmDialog(QDialog):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()


    def initUI(self):
        self.resize(400, 250)
        self.setStyleSheet("background-color:#E5E9F5;")
        self.center()
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel(self.text)
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label

        btnOK = QPushButton("확인")
        btnOK.resize(100, 50)
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnOK.setStyleSheet("""
                    QPushButton {
                        margin: 35px 0px 50px 0px;
                        background-color: #85B6FF;
                        border: 1px solid;
                        border-radius: 5px;
                        font: bold;
                        font-size: 20px;
                    }
                    QPushButton:hover {
                        background-color: #FEBB61;
                    }
                """)

        layout.addWidget(label)
        layout.addWidget(btnOK)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def showModal(self):
        return super().exec_()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())