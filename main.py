# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
#
# one gui create by hzh

# a function for open camera,close camera,open image and movie

# EigenFaces  FisherFaces  LBPH

from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QKeyEvent
import cv2
import time
import os

import face_detect

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer_camera = QtCore.QTimer()  # 定时器
        self.setupUi()
        self.retranslateUi()

        self.path = ""   #先定义path

        self.slot_init()  # 设置槽函数
        #self.keyPressEvent()  #设置按键函数
        self.show()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(992, 600)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 60, 200, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton_op = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_op.setObjectName("pushButton_open")
        self.verticalLayout.addWidget(self.pushButton_op)
        self.pushButton_save = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.verticalLayout.addWidget(self.pushButton_save)
        self.pushButton_sta = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_sta.setObjectName("pushButton_start")
        self.verticalLayout.addWidget(self.pushButton_sta)
        self.pushButton_cls = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_cls.setObjectName("pushButton_close")
        self.verticalLayout.addWidget(self.pushButton_cls)
        self.pushButton_detect = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_detect.setObjectName("pushButton_detect")
        self.verticalLayout.addWidget(self.pushButton_detect)
        self.pushButton_id = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_id.setObjectName("pushButton_id")
        self.verticalLayout.addWidget(self.pushButton_id)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 40, 600, 450))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 992, 26))
        self.menubar.setObjectName("menubar")
        self.menucapture = QtWidgets.QMenu(self.menubar)
        self.menucapture.setObjectName("menucapture")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        self.actionopen_image = QtWidgets.QAction(self)
        self.actionopen_image.setObjectName("actionopen_image")
        self.actionsave_image = QtWidgets.QAction(self)
        self.actionsave_image.setObjectName("actionsave_image")

        self.menucapture.addAction(self.actionopen_image)
        self.menucapture.addAction(self.actionsave_image)
        self.menubar.addAction(self.menucapture.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "hzhsfirstpyqt5"))
        self.pushButton_op.setText(_translate("MainWindow", "open"))
        self.pushButton_save.setText(_translate("MainWindow", "save"))
        self.pushButton_sta.setText(_translate("MainWindow", "start"))
        self.pushButton_cls.setText(_translate("MainWindow", "close"))
        self.pushButton_detect.setText(_translate("MainWindow", "detect face"))
        self.pushButton_id.setText(_translate("MainWindow", "save id"))

        self.label.setText(_translate("MainWindow", "player"))
        self.menucapture.setTitle(_translate("MainWindow", "capture"))
        self.actionopen_image.setText(_translate("MainWindow", "open image"))
        self.actionsave_image.setText(_translate("MainWindow", "save image"))

    def slot_init(self):
        self.pushButton_op.clicked.connect(self.open_image)
        self.pushButton_sta.clicked.connect(self.open_camera)
        self.timer_camera.timeout.connect(self.cat_image)
        self.pushButton_detect.clicked.connect(self.face_detect)
        self.pushButton_cls.clicked.connect(self.close_camera)
        self.pushButton_save.clicked.connect(self.save_image)
        self.pushButton_id.clicked.connect(self.save_id)


    # 打开文件有以下3种：
    # 1、单个文件打开 QFileDialog.getOpenFileName()
    # 2、多个文件打开 QFileDialog.getOpenFileNames()
    # 3、打开文件夹 QFileDialog.getExistingDirectory()
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            self.cap.release()
        #print(event.key())
    # #     #return super().keyPressEvent(event)

    def open_image(self):
        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "openfile", "./image",
                                                        "image(*.jpg;*.png;*.gif;*.bmp;*.mp4;*.avi)")
        # self 改为None,不然报错为argument 1 has unexpected type 'Ui_MainWindow',过滤条件之间要用；分开而不是逗号
        # 返回值为path,filter str
        if self.path != "":   #None 和“”区别很大
            imgtype = self.path.split(".")[-1]
            if imgtype == "jpg" or imgtype == "png" or imgtype == "gif" or imgtype == "bmp":
                self.img = cv2.imread(self.path)
                self.show_image()
            else:
                self.cap = cv2.VideoCapture(self.path)
                while True:
                    ret, self.img = self.cap.read()
                    if ret==True:
                        self.show_image()
                        cv2.waitKey(30)
                    else:
                        self.cap.release()
                        break

    def face_detect(self):
        if self.path != "":
            imgtype = self.path.split(".")[-1]
            if imgtype == "jpg" or imgtype == "png" or imgtype == "gif" or imgtype == "bmp":
                self.img = cv2.imread(self.path)
                self.img,self.face_area = face_detect.face_detect(self.img)
                self.show_image()
            else:
                self.cap = cv2.VideoCapture(self.path)
                while True:
                    ret, self.img = self.cap.read()
                    if ret == True:
                        self.img,self.face_area = face_detect.face_detect(self.img)
                        self.show_image()
                        cv2.waitKey(25)
                    else:
                        self.cap.release()
                        break

    def open_camera(self):
        self.cap = cv2.VideoCapture()  # 准备获取图像
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(0)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                    self, u"Warning", u"请检测相机与电脑是否连接正确",
                    buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(20)

    def cat_image(self):

        ret, self.image = self.cap.read()

        self.image = cv2.flip(self.image, 1)  # 左右翻转
        # detect
        self.img,self.face_area = face_detect.face_detect(self.image)
        self.show_image()

    # 对图像进行处理，放入到label中显示
    def show_image(self):

        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)  # 颜色转换
        #self.face_detect()
        #self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        showimg = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], QtGui.QImage.Format_RGB888) #彩图显示
        #showimg = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], QtGui.QImage.Format_Indexed8)  #灰度图像这样显示

        self.label.setPixmap(QtGui.QPixmap.fromImage(showimg))
        self.label.setScaledContents(True)



    def close_camera(self):
        if self.timer_camera.isActive() != False:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()

    def save_image(self):
        now = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        if os.path.exists("./image")==False :
            os.makedirs("./image")
        #self.image=cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("./image/" + now + ".jpg", self.image)

    def save_id(self):
        #获取人脸id
        self.id,ok = QtWidgets.QInputDialog.getText(self,"new_face_id","your name:",QtWidgets.QLineEdit.Normal,"")

        if os.path.exists("./model")==False :
            os.makedirs("./model")

        if ok and len(self.id) != 0:
            id_path="./model/" + self.id
            #判断是否有过id
            if os.path.exists(id_path) == False:
                os.makedirs(id_path)
            if len(os.listdir(id_path)) >= 500:
                QtWidgets.QMessageBox.information(self, "message",self.id + " has already existed")
            while len(os.listdir(id_path)) < 500:
                self.cat_image()
                if len(self.face_area) != 0:
                    now = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
                    cv2.imwrite(id_path + "/"+now + ".jpg", self.face_area)
            QtWidgets.QMessageBox.information(self,"message",
                                              "the face image of "+self.id+" has been saved for 100 pics")


if __name__ == '__main__':
    app = QApplication(argv)
    ui = Ui_MainWindow()

    if app.exec() == False:
        ui.close_camera()  # 按窗口× ，关闭摄像头程序
        exit(app.exec_())