import os

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView
from loguru import logger as log

script_path = r'../pyqt/scripts/'

def load_script(self):
    """加载脚本"""
    log.info(f'加载脚本')
    # 获取目录文件
    script_file_list = os.listdir(script_path)
    script_file_list.pop(script_file_list.index('__init__.py'))
    script_file_list.pop(script_file_list.index('__pycache__'))

    # listView_load_script 加载内容
    model = QStandardItemModel()
    # 向模型中添加数据
    for script_file in script_file_list:
        model.appendRow(QStandardItem(script_file))
    # 将模型设置到 listView
    self.listView_load_script.setModel(model)
    self.listView_load_script.setSelectionMode(QListView.ExtendedSelection)


def add_script(self):
    # 获取listView_load_script选中的内容
    indexes = self.listView_load_script.selectedIndexes()

    model = QStandardItemModel()
    for index in indexes:
        script_name = index.data()
        log.debug(script_name)
        model.appendRow(QStandardItem(script_name))
    self.listView_run_script.setModel(model)
    self.listView_run_script.setSelectionMode(QListView.ExtendedSelection)

def run_script(self):
    pass