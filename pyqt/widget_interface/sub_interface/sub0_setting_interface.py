from PyQt5.QtWidgets import QWidget
from pyqt.ui.sub_ui.sub0_setting import Ui_Form
import pyqt.data.app_data_define.ui_data as ui_data


class SettingInterface(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(ui_data.SETTING_NAME)
        self.parent_window = parent
        self.init_widget()

    def init_widget(self):
        pass
