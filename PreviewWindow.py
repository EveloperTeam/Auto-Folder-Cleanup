import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from collections import deque
import os
import pandas as pd

class PreviewWindow(QDialog):
    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir
        self.initUI()


    def importDataLeft(self, dir_list, file_list, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        parent = root
        for dir in dir_list:
            icon = QIcon('./img/folder.png')
            item = QStandardItem(icon, dir)
            parent.appendRow(item)

        for file in file_list:
            icon = QIcon('./img/file.png')
            item = QStandardItem(icon, file)
            parent.appendRow(item)

    def importDataRight(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        parent = root

        for i in range(len(data)):
            folder = QStandardItem(QIcon('./img/folder.png'), '폴더' + str(i+1))
            parent.appendRow(folder)
            for j in range(len(data[i])):
                file = QStandardItem(QIcon('./img/file.png'), data[i][j])
                folder.appendRow(file)

    def initUI(self):
        self.setWindowTitle('미리보기')
        self.resize(1000, 1000)
        self.setStyleSheet("background-color:#E5E9F5;")
        self.center()

        #Setup Data
        data = pd.read_csv('./data.csv')
        data = data.sort_values(by='cluster')
        data = data.groupby('cluster')['origin'].apply(list)
        data = data.to_list()

        #root_dir = '/Users/andonghyun/Downloads/새 폴더'
        target_folder = self.root_dir.split('/')[-1]
        all_list = os.listdir(self.root_dir)

        file_list = []
        dir_list = []
        for item in all_list:
            path = self.root_dir + '/' + item

            if os.path.isfile(path):
                file_list.append(item)
            if os.path.isdir(path):
                dir_list.append(item)

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

        # Label 설정
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

        # Button 설정
        btnOK = QPushButton()
        btnOK.clicked.connect(lambda : self.onOKButtonClicked(data, self.root_dir))
        btnOK.setIcon(QIcon('./img/check.png'))
        btnOK.setStyleSheet("border-radius:15px; border:2px solid black; background-color:#00DC58; padding:20px;")

        btnCancel = QPushButton()
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        btnCancel.setIcon(QIcon('./img/close.png'))
        btnCancel.setStyleSheet("border-radius:15px; border:2px solid black; background-color:#FF0000; padding:20px;")


        # 위젯 추가
        TitleLayout.addWidget(previewImg)
        TitleLayout.addWidget(titleLabel)
        TitleLayout.setAlignment(Qt.AlignLeft)


        # Left & Right TreeView (Folder Hierarchy)

        #Setup LeftTreeView
        LeftTreeView = QTreeView()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(LeftTreeView)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([target_folder])
        LeftTreeView.header().setDefaultSectionSize(200)
        LeftTreeView.header().setFixedHeight(40)
        LeftTreeView.setModel(self.model)
        self.importDataLeft(dir_list, file_list)

        LeftTreeView.setSelectionMode(LeftTreeView.SingleSelection)
        LeftTreeView.setDragDropMode(QAbstractItemView.InternalMove)
        LeftTreeView.setDragEnabled(True)
        LeftTreeView.setAcceptDrops(True)
        LeftTreeView.setDropIndicatorShown(True)
        LeftTreeView.expandAll()

        #Setup RightTreeView
        RightTreeView = QTreeView()
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(RightTreeView)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([target_folder])
        RightTreeView.header().setDefaultSectionSize(200)
        RightTreeView.header().setFixedHeight(40)
        RightTreeView.setModel(self.model)
        self.importDataRight(data)

        RightTreeView.setSelectionMode(RightTreeView.SingleSelection)
        RightTreeView.setDragDropMode(QAbstractItemView.InternalMove)
        RightTreeView.setDragEnabled(True)
        RightTreeView.setAcceptDrops(True)
        RightTreeView.setDropIndicatorShown(True)
        RightTreeView.expandAll()

        #TreeView StyleSheet
        LeftTreeView.setStyleSheet(
            'background-color : #85B6FF;'
            'border : none;'
            'font: 23px;'
        )

        RightTreeView.setStyleSheet(
            'background-color : #85B6FF;'
            'border : none;'
            'font: 23px;'
        )

        LeftGroupBox.setLayout(leftLayout)
        RightGroupBox.setLayout(rightLayout)

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

    def onOKButtonClicked(self, data, root_dir):
        '''
        for i in range(len(data)):
            folder_path = self.root_dir + '/' + '폴더' + str(i+1)
            try:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            except OSError:
                print('Error: Creating directory. ' + folder_path)

            for j in range(len(data[i])):
                origin_file_path = self.root_dir + '/' + data[i][j]
                new_file_path = folder_path + '/' + data[i][j]
                os.replace(origin_file_path, new_file_path)
        '''
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