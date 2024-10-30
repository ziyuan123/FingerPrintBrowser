# -*- coding: utf-8 -*-
from PyQt5.QtGui import QDesktopServices, QPen, QColor, QTextDocument, QFont, QTextCursor, QTextCharFormat

from PyQt5.QtWidgets import QStyledItemDelegate, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QListWidget
from PyQt5.QtCore import Qt, QUrl, QEvent


class HyperlinkDelegate(QStyledItemDelegate):
    """
    用于在Qt界面中处理超链接的显示和鼠标点击事件，通过重写QStyledItemDelegate类的几个方法实现
    """

    def __init__(self, parent=None):
        super(HyperlinkDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return None  # 不创建编辑器，因为我们只处理显示

    def setEditorData(self, editor, index):
        pass  # 为空，不执行任何操作，因为不支持编辑

    def updateEditorGeometry(self, editor, option, index):
        pass  # 为空，不执行任何操作，因为不支持编辑

    def paint(self, painter, option, index):
        # 用于绘制文本和超链接
        # 从index中获取显示文本，使用painter绘制文本
        text = index.model().data(index, Qt.DisplayRole)
        painter.save()

        # 设置字体
        painter.setPen(Qt.blue)  # 蓝色、下划线字体
        font = painter.font()
        font.setUnderline(True)
        painter.setFont(font)

        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        # 处理鼠标点击事件。
        # 当鼠标左键释放时，从index中获取Qt.UserRole角色对应的URL
        # 并使用QDesktopServices.openUrl打开URL。
        # 返回False表示事件未被处理
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            url = QUrl(index.model().data(index, Qt.UserRole))
            QDesktopServices.openUrl(url)
        return False


class RangeInputDialog(QDialog):
    def __init__(self, user_list=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("输入导入范围")

        self.layout = QVBoxLayout()

        if user_list is not None:
            user_list_add_index = []
            for index, user in enumerate(user_list):
                user_list_add_index.append(f"{index+1}: {user}")
            # 添加一个 QListWidget 来显示列表
            self.listWidget = QListWidget()
            self.listWidget.addItems(user_list_add_index)
            self.layout.addWidget(self.listWidget)

        self.label_min = QLabel("from:")
        self.input_min = QLineEdit()
        self.layout.addWidget(self.label_min)
        self.layout.addWidget(self.input_min)

        self.label_max = QLabel("to:")
        self.input_max = QLineEdit()
        self.layout.addWidget(self.label_max)
        self.layout.addWidget(self.input_max)

        self.button = QPushButton("确认")
        self.button.clicked.connect(self.validate_input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.result = (None, None)

    def validate_input(self):
        try:
            minValue = int(self.input_min.text())
            maxValue = int(self.input_max.text())
            if minValue > maxValue:
                QMessageBox.warning(self, "警告", "from值不能大于to")
            else:
                self.result = (minValue, maxValue)
                self.accept()
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的整数")