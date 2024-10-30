# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, FluentIcon, InfoBarPosition
from loguru import logger as log


class ShowInfo:

    def __init__(self, parent: QWidget):
        self.parent = parent

    def create_info_info_bar(self, title='', content=''):
        """显示信息窗口"""
        content = content
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title=title,
            content=content,
            orient=Qt.Vertical,  # vertical layout
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self.parent
        )
        log.info('\n{}: \n  {}', title, content)
        w.addWidget(PushButton('Action'))
        w.show()

    def create_success_info_bar(self, title='', content=''):
        """显示成功窗口"""
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=5000,
            parent=self.parent
        )
        log.debug('\n{}: \n {}', title, content)

    def create_warning_info_bar(self, title='', content=''):
        """显示警告窗口"""
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=False,  # disable close button
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self.parent
        )
        log.warning('\n{}: \n   {}', title, content)

    def create_error_info_bar(self, title='', content=''):
        """显示错误窗口"""
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,  # won't disappear automatically
            parent=self.parent
        )
        log.error('\n{}: \n {}', title, content)

    def create_custom_info_bar(self, title='', content=''):
        """显示风格窗口"""
        w = InfoBar.new(
            icon=FluentIcon.GITHUB,
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self.parent
        )
        log.debug('\n{}: \n {}', title, content)
        w.setCustomBackgroundColor('white', '#202020')
