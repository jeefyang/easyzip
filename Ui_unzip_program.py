# Form implementation generated from reading ui file 'd:\knowledge\toy\py\easyZip\unzip_program.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plain_unzip_progress = QtWidgets.QTextEdit(parent=self.frame)
        self.plain_unzip_progress.setEnabled(True)
        self.plain_unzip_progress.setObjectName("plain_unzip_progress")
        self.gridLayout_2.addWidget(self.plain_unzip_progress, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(parent=Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(parent=self.frame_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label.setObjectName("label")
        self.label_unzip_progress = QtWidgets.QLabel(parent=self.frame_2)
        self.label_unzip_progress.setGeometry(QtCore.QRect(40, 10, 261, 16))
        self.label_unzip_progress.setObjectName("label_unzip_progress")
        self.btn_unzip_stop = QtWidgets.QPushButton(parent=self.frame_2)
        self.btn_unzip_stop.setGeometry(QtCore.QRect(280, 40, 51, 21))
        self.btn_unzip_stop.setObjectName("btn_unzip_stop")
        self.btn_unzip_continue = QtWidgets.QPushButton(parent=self.frame_2)
        self.btn_unzip_continue.setGeometry(QtCore.QRect(340, 40, 51, 21))
        self.btn_unzip_continue.setObjectName("btn_unzip_continue")
        self.btn_unzip_close = QtWidgets.QPushButton(parent=self.frame_2)
        self.btn_unzip_close.setGeometry(QtCore.QRect(400, 40, 51, 21))
        self.btn_unzip_close.setObjectName("btn_unzip_close")
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "进度:"))
        self.label_unzip_progress.setText(_translate("Dialog", "准备待续"))
        self.btn_unzip_stop.setToolTip(_translate("Dialog", "<html><head/><body><p>asdas</p></body></html>"))
        self.btn_unzip_stop.setText(_translate("Dialog", "暂停"))
        self.btn_unzip_continue.setText(_translate("Dialog", "继续"))
        self.btn_unzip_close.setText(_translate("Dialog", "关闭"))
