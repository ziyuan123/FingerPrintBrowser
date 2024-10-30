# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

import pyqt.data.app_data_define.ui_data as ui_data
from pyqt.ui.sub_ui.sub2_get_aim_info import Ui_Form
from library.qt_lib.show_info_bar import ShowInfo


class GetAimInfoInterface(QWidget, Ui_Form):

    def __init__(self, parent_window, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(ui_data.SUB2_NAME)
        self.parent_window = parent_window

        self.show_info = ShowInfo(self)
        self.init_widget()

    def init_widget(self):
        pass
