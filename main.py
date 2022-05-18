import os
import sys
import time as tm

import pandas as pd
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from models.dataprocess import data_processing
from models.translation import lan_analysis, lan_translation
from PreviewWindow import PreviewWindow
from models.embedding import embedding


class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.f_list = []
        self.dir = []

        label = QLabel('정리할 폴더를 선택하세요.', self)
        label.setStyleSheet("margin: 3em 0em 0em 9em; font: bold; font-size: 20px")

        open_btn = QPushButton('', self)
        open_btn.setMaximumWidth(35)
        open_btn.setMinimumHeight(35)
        open_btn.setIcon(QIcon('./img/opened-folder.png'))
        open_btn.setIconSize(QSize(30, 30))
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #85B6FF;
                border: 1px solid;
                border-radius: 5px;
                margin: 3em 0em 0em 0em;
            }
            QPushButton:hover {
                background-color: #FEBB61;
            }
        """)
        open_btn.clicked.connect(self.open_folder)

        self.file_list = QTextEdit()
        self.file_list.setAcceptRichText(False)
        self.file_list.setReadOnly(True)
        self.file_list.setMaximumWidth(2500)
        self.file_list.setMinimumHeight(50)
        self.file_list.setStyleSheet(
            "margin: 0px 200px 10px 200px;"
            "background-color: #FFFFFF;"
            "border: 1px solid;"
            "border-radius: 10px"
        )

        delete_btn = QPushButton('', self)
        delete_btn.setMaximumWidth(35)
        delete_btn.setMinimumHeight(35)
        delete_btn.setIcon(QIcon('./img/delete.png'))
        delete_btn.setIconSize(QSize(30, 30))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #85B6FF;
                border: 1px solid;
                border-radius: 5px;
                margin: 3em 0em 0em 0em;
            }
            QPushButton:hover {
                background-color: #FEBB61;
            }
        """)
        delete_btn.clicked.connect(self.delete_folder)

        start_btn = QPushButton(' 정리 시작', self)
        start_btn.setMaximumWidth(200)
        start_btn.setMinimumHeight(45)
        start_btn.setIcon(QIcon('./img/start.png'))
        start_btn.setIconSize(QSize(30, 30))
        start_btn.setStyleSheet("""
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
        start_btn.clicked.connect(self.open_preview)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(label, 0, 0)
        grid.addWidget(open_btn, 0, 2, Qt.AlignRight)
        grid.addWidget(delete_btn, 0, 3)
        grid.addWidget(self.file_list, 1, 0, 1, 5)
        grid.addWidget(start_btn, 2, 0, 1, 5, Qt.AlignCenter)

    def open_folder(self):
        dname = QFileDialog.getExistingDirectory(self, 'Open file', './')
        if(dname not in self.dir):
            f_list = os.listdir(dname)
            self.dir.append(dname)
            self.f_list.append(f_list)
            #print(f_list)
            for file in f_list:
                exist = self.file_list.toPlainText()
                self.file_list.setText(exist + file + '\n')

                # self.file_list.setText(exist + dname + '/' + file + '\n') dname == 경로

    def delete_folder(self):
        self.file_list.clear()
        self.f_list = []
        self.dir = []

    def open_preview(self):
        win = PreviewWindow()
        print(self.f_list)
        data_processing(self.dir, self.f_list)


        data = pd.read_csv("./data.csv")
        # print(data)
        self.f_list = data['no-ext'].values.tolist() # data.csv의 [1]번째 열을 리스트로 변환
        lan_list = lan_analysis(self.f_list)
        trans_list = lan_translation(self.f_list, lan_list)
        # print("trans_list: ", trans_list)
        data['trans'] = trans_list
        data.to_csv("./data.csv", index=False)

        embedding()


        r = win.showModal()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(229, 233, 245))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        mp = MainPage()
        self.setCentralWidget(mp)

        self.setWindowTitle('Clean Folder')
        self.setWindowIcon(QIcon('./img/logo.png'))
        self.setGeometry(300, 250, 1440, 1024) # (x, y, w, h)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_pix = QPixmap('./img/splash.png')
    splash_pix = splash_pix.scaled(720, 512)

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progressBar = QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(10, splash_pix.height() - 10, splash_pix.width() - 5, 20)

    splash.show()

    for i in range(1, 11):
        progressBar.setValue(i)
        pt = tm.time()
        while tm.time() < pt + 0.1:
           app.processEvents()

    tm.sleep(1)

    ex = MainWindow()
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())