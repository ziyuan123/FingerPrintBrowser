# -*- coding: utf-8 -*-
import os.path
import sys
import time
import traceback

from loguru import logger as log
from library.config.log_config import config_log
from PyQt5.QtWidgets import QApplication
from pyqt.widget_interface.main_window import MainWindow

def custom_excepthook(exc_type, exc_value, exc_traceback):
    # 打印异常信息到日志文件
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    error_message = '\n错误时间：{}\n错误类型：{}\n错误原因：{}\n错误追踪：{}'.format(
        time_now, exc_type, exc_value, traceback.extract_tb(exc_traceback))
    log.error(error_message)
    traceback.print_exception(exc_type, exc_value, exc_traceback)

if __name__ == "__main__":
    config_log()
    sys.excepthook = custom_excepthook
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()
    except Exception as e:
        log.exception(e)
