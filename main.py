# -*- coding: utf-8 -*-
"""main GUI file of clustering by Feng Hao 5/27/2018"""
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import main_of_sc
import icons


class Cluster(QtWidgets.QMainWindow):

    cluster_method = 2
    get_path = ''
    out_path = ''
    vnumber = 3
    knumber = 4
    step = 0

    def __init__(self):
        super(Cluster, self).__init__()                         # 使用super来调用父辈初始化函数

        self.setWindowTitle("Clustering Man")                   # 程序标题
        self.setWindowIcon(QtGui.QIcon(r':ic/wake.ico'))
        self.statusBar().showMessage('Standing by')             # 状态栏
        self.resize(640, 480)

        self.main_ground = QtWidgets.QWidget()                  # 主窗口
        self.setCentralWidget(self.main_ground)

        self.create_clustermethod()                             # 选择聚类方法的窗口
        self.create_parameter()                                 # 选择聚类参数的窗口
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setStatusTip("It tells you the progress of clustering")

        self.file_open = QtWidgets.QAction(QtGui.QIcon(r":ic/open.ico"), "Open file", self)   # 打开文件的选项
        self.file_open.setShortcut("Ctrl+O")
        self.file_open.setStatusTip("Open file")
        self.file_open.triggered.connect(self.show_dialog)

        self.file_out = QtWidgets.QAction(QtGui.QIcon(r":ic/out.ico"), "Output path", self)     # 输出分类文件的路径
        self.file_out.setShortcut("Ctrl+1")
        self.file_out.setStatusTip("Choose output path")
        self.file_out.triggered.connect(self.show_outdialog)

        self.information_button = QtWidgets.QAction(QtGui.QIcon(r":ic/question.ico"), "Help", self)  # 软件的说明
        self.information_button.setShortcut("Ctrl+2")
        self.information_button.setStatusTip("Supporting information")
        self.information_button.triggered.connect(self.show_information)

        self.quit_button = QtWidgets.QPushButton("Exit", self)       # 退出按钮
        self.quit_button.resize(64, 48)
        self.quit_button.setStatusTip("Exit procedure")
        self.quit_button.clicked.connect(QtWidgets.qApp.quit)

        self.start_button = QtWidgets.QPushButton("Start", self)        # 开始按钮
        self.start_button.resize(64, 48)
        self.start_button.setStatusTip("Start clustering")
        self.start_button.clicked.connect(self.start_clustering)

        self.toolbar = self.addToolBar("Option")                 # 创建工具栏
        self.toolbar.addAction(self.file_open)
        self.toolbar.addAction(self.file_out)
        self.toolbar.addAction(self.information_button)

        self.main_grid = QtWidgets.QGridLayout()             # 对布局进行设计
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.addWidget(self.clustermethodGroupBox)
        self.hboxlayout.addWidget(self.parameterGroupBox)
        self.main_grid.addWidget(QtWidgets.QLabel(''), 1, 0)
        self.main_grid.addLayout(self.hboxlayout, 2, 0, 7, 9)
        self.main_grid.addWidget(QtWidgets.QLabel(''), 9, 0)
        self.main_grid.addWidget(QtWidgets.QLabel('Progress:'), 10, 1)
        self.main_grid.addWidget(self.pbar, 10, 2, 1, 6)
        self.main_grid.addWidget(QtWidgets.QLabel(''), 11, 0)
        self.main_grid.addWidget(self.start_button, 12, 7)
        self.main_grid.addWidget(self.quit_button, 12, 8)
        self.main_ground.setLayout(self.main_grid)

    def create_clustermethod(self):
        self.clustermethodGroupBox = QtWidgets.QGroupBox("Clustering Method")       # 布局GroupBox
        layout = QtWidgets.QGridLayout()
        self.fastway = QtWidgets.QRadioButton("Quick Clustering", self)
        self.fastway.setIcon(QtGui.QIcon(r":ic/fast.png"))
        self.fastway.setStatusTip("K-means clustering")
        self.slowway = QtWidgets.QRadioButton("Accurate Clustering", self)
        self.slowway.setIcon(QtGui.QIcon(r":ic/slow.ico"))
        self.slowway.setStatusTip("Spectral clustering")
        self.cluster_choice = QtWidgets.QButtonGroup(self)               # 用一个Group来绑定单选框
        self.cluster_choice.addButton(self.fastway, 0)
        self.cluster_choice.addButton(self.slowway, 1)
        self.cluster_choice.buttonClicked.connect(self.clusterchoice)

        layout.addWidget(self.fastway, 0, 1)                           # 采用网络布局的方法
        layout.addWidget(QtWidgets.QLabel(''), 0, 0)
        layout.addWidget(QtWidgets.QLabel(''), 4, 4)
        layout.addWidget(self.slowway, 4, 1)
        self.clustermethodGroupBox.setLayout(layout)

    def clusterchoice(self):                                       # 聚类方法的选择
        if self.cluster_choice.checkedId() == 0:
            self.cluster_method = 0
            self.Vlabel.setEnabled(1)
            self.Vbutton.setEnabled(1)
        elif self.cluster_choice.checkedId() == 1:
            self.cluster_method = 1
            self.Vlabel.setEnabled(0)
            self.Vbutton.setEnabled(0)

    def create_parameter(self):
        self.parameterGroupBox = QtWidgets.QGroupBox("Clustering parameter")
        layout = QtWidgets.QGridLayout()
        
        label1 = QtWidgets.QLabel("PC quantity:")
        self.Vlabel = QtWidgets.QLabel("3")
        self.Vlabel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.Vbutton = QtWidgets.QPushButton("...")
        self.Vbutton.clicked.connect(self.selectV)
        self.Vbutton.setStatusTip("Different principal component quantity may cause different "
                                  "results, try many times")

        label2 = QtWidgets.QLabel("Category quantity:")
        self.Klabel = QtWidgets.QLabel("4")
        self.Klabel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.Kbutton = QtWidgets.QPushButton("...")
        self.Kbutton.clicked.connect(self.selectK)
        self.Kbutton.setStatusTip("It depends on how many categories you want")

        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.Vlabel, 0, 1)
        layout.addWidget(self.Vbutton, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.Klabel, 1, 1)
        layout.addWidget(self.Kbutton, 1, 2)
        self.parameterGroupBox.setLayout(layout)

    def selectV(self):
        number, ok = QtWidgets.QInputDialog.getInt(self, "Principal Component quantity", "Please choose the "
                                                                                         "quantity of PC",
                                                   int(self.Vlabel.text()), 1, 1000, 1)
        if ok:
            self.Vlabel.setText(str(number))
            self.vnumber = int(number)

    def selectK(self):
        number, ok = QtWidgets.QInputDialog.getInt(self, "Category quantity", "Please choose the quantity of category",
                                                   int(self.Klabel.text()), 1, 1000, 1)
        if ok:
            self.Klabel.setText(str(number))
            self.knumber = int(number)

    def center(self):                                   # 调整窗口到屏幕中间
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Exit', 'Have you finished all of your clustering tasks?',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show_dialog(self):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose the path of input', r"G:\desktop")
        self.get_path = file_name

    def show_outdialog(self):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose the path of output', r"G:\desktop")
        self.out_path = file_name

    def show_information(self):
        reply = QtWidgets.QMessageBox.information(self, "Supporting information", " This program is used to classify"
                                                                                  " pictures into different categories,"
                                                                                  " which allows you to choose k-means "
                                                                                  "algorithm or spectral clustering "
                                                                                  "algorithm. The first algorithm is "
                                                                                  "quick but less accurate while the "
                                                                                  "other one is accurate but it may "
                                                                                  "take much more time. ",
                                                  QtWidgets.QMessageBox.Yes)

    def start_clustering(self):
        self.step = 0
        condition = main_of_sc.clustercore(self.cluster_method, self.get_path, self.out_path, self.vnumber,
                                           self.knumber, self.step, self.pbar)
        if condition == 0:                           # 应对不同的情况报错
            QtWidgets.QMessageBox.warning(self, "ERROR PATH", "Please set the path of input or output!",
                                          QtWidgets.QMessageBox.Yes)
        if condition == 1:
            QtWidgets.QMessageBox.warning(self, "ERROR METHOD", "Please choose one method of clustering",
                                          QtWidgets.QMessageBox.Yes)
        if condition == 2:
            QtWidgets.QMessageBox.warning(self, "NO PICTURES", "No pictures in this input path",
                                          QtWidgets.QMessageBox.Yes)
        if condition == 3:
            QtWidgets.QMessageBox.information(self, "SUCCESS", "All done!", QtWidgets.QMessageBox.Yes)

app = QtWidgets.QApplication(sys.argv)
cl = Cluster()
cl.center()
cl.show()
sys.exit(app.exec_())
