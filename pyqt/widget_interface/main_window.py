# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationItemPosition, NavigationAvatarWidget

from library.qt_lib.show_info_bar import ShowInfo
from pyqt.data.app_data_define import ui_data
from pyqt.widget_interface.sub_interface.sub0_setting_interface import SettingInterface
from pyqt.widget_interface.sub_interface.sub1_home_interface import HomeInterface
from pyqt.widget_interface.sub_interface.sub2_get_aim_info import GetAimInfoInterface

class MainWindow(SplitFluentWindow):
    local_account_list = []

    def __init__(self):
        super().__init__()
        self.show_info = ShowInfo(self)

        self.init_window()

        # 配置子界面
        self.setting_interface = SettingInterface(self)
        self.home_interface = HomeInterface(self)
        self.sub2_get_aim_info = GetAimInfoInterface(self)
        self.load_interface()

    def init_window(self):
        self.setWindowTitle(ui_data.APPLICATION_NAME)
        self.setWindowIcon(QIcon(ui_data.APPLICATION_IMAGE))
        self.resize(800, 800)
        self.init_them()

    def init_them(self):
        # 设置窗口效果
        # self.windowEffect.setAeroEffect(self.winId())
        pass

    def change_theme(self):
        pass
        # toggleTheme()
        # self.setWindowOpacity(0.97)  # 设置窗口背景透明度

    def load_interface(self):
        self.addSubInterface(self.home_interface, FluentIcon.HOME, '主页')
        self.addSubInterface(self.sub2_get_aim_info, FluentIcon.ACCEPT_MEDIUM, '测试')
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('主题', ui_data.APPLICATION_IMAGE),
            position=NavigationItemPosition.BOTTOM,
            onClick=self.change_theme
        )
        self.addSubInterface(self.setting_interface, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)