# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sub0_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(40, 40, 241, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.LineEdit_port = LineEdit(self.groupBox)
        self.LineEdit_port.setGeometry(QtCore.QRect(80, 40, 63, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LineEdit_port.setFont(font)
        self.LineEdit_port.setPlaceholderText("")
        self.LineEdit_port.setObjectName("LineEdit_port")
        self.StrongBodyLabel_17 = StrongBodyLabel(self.groupBox)
        self.StrongBodyLabel_17.setGeometry(QtCore.QRect(10, 40, 72, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.StrongBodyLabel_17.setFont(font)
        self.StrongBodyLabel_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.StrongBodyLabel_17.setObjectName("StrongBodyLabel_17")
        self.PrimaryPushButton_save_setting = PrimaryPushButton(self.groupBox)
        self.PrimaryPushButton_save_setting.setGeometry(QtCore.QRect(160, 40, 75, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_save_setting.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_save_setting.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PrimaryPushButton_save_setting.setFont(font)
        self.PrimaryPushButton_save_setting.setObjectName("PrimaryPushButton_save_setting")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "软件设置"))
        self.LineEdit_port.setText(_translate("Form", "10"))
        self.StrongBodyLabel_17.setText(_translate("Form", "代理端口"))
        self.PrimaryPushButton_save_setting.setText(_translate("Form", "保存设置"))
from qfluentwidgets import LineEdit, PrimaryPushButton, StrongBodyLabel
