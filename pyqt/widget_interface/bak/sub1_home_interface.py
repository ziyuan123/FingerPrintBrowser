# -*- coding: utf-8 -*-
import importlib
import os
import sys
import pprint

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from idna.idnadata import scripts
from loguru import logger as log
import sqlite3

from library.qt_lib import init_section

from PyQt5.QtWidgets import QWidget, QMenu, QAction

from library.qt_lib.thread import ChromeThread, MyThread
from pyqt.app_function import handle_env_config_db, handle_script
from pyqt.data.app_data_define import db_data
from pyqt.data.app_data_define import ui_data
from pyqt.data.data_struct.data_struct import ChromeInfo
from pyqt.ui.sub_ui.sub1_home import Ui_Form
from library.qt_lib.show_info_bar import ShowInfo


class HomeInterface(QWidget, Ui_Form):
    thread = None
    started_chrome_info_dict = {}
    timer = None

    def __init__(self, parent_window, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(ui_data.HOME_NAME)
        self.parent_window = parent_window
        self.show_info = ShowInfo(self)

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_chrome_status)
        self.timer.setInterval(10000)

        self.init_widget()

    def init_widget(self):
        self.init_button()
        self.init_table_view()
        self.init_menu()
        self.timer.start()

    def test(self):
        log.debug(pprint.pformat(self.started_chrome_info_dict))

    def run_script_test(self):
        # 获取self.listView_load_script中的所有内容
        model = self.listView_run_script.model()
        all_file_name = []
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            file_name = model.data(index, Qt.DisplayRole)
            all_file_name.append(file_name)

        # 导入内容
        for file_name in all_file_name:
            log.debug(file_name)
            file_name = file_name.replace('.py', '')
            module = importlib.import_module(f'pyqt.scripts.{file_name}')
            # 检查模块中是否存在 run_action 函数
            if hasattr(module, 'run_action'):
                run_action = getattr(module, 'run_action')
                # 调用 run_action 函数并传递 driver 参数
                run_action(self.started_chrome_info_dict['1'].driver)
                log.debug(f"成功调用 {file_name}.run_action")
            else:
                log.warning(f"模块 {file_name} 中没有 run_action 函数")

    def init_button(self):
        self.PrimaryPushButton_test.clicked.connect(self.test)
        self.PrimaryPushButton_load_script.clicked.connect(lambda: handle_script.load_script(self))
        self.PrimaryPushButton_add_script.clicked.connect(lambda: handle_script.add_script(self))
        self.PrimaryPushButton_run_script.clicked.connect(lambda: self.run_script())

    def run_script(self):
        log.debug('run script')
        # 获取脚本执行配置
        try:
            _from = int(self.lineEdit_from.text())
            _to = int(self.lineEdit_to.text())
            thread_count = int(self.spinBox_thread_count.text())
            if _from > _to:
                raise Exception('错误：from 不能大于 to')
        except Exception as e:
            self.show_info.create_warning_info_bar('请输入正确的浏览器范围：from、to', str(e))
            return
        log.debug(f'from:{_from}, to:{_to}, thread_count:{thread_count}')

        # 浏览器分组
        env_num_group_list = [list(range(i, min(i + thread_count, _to + 1))) for i in range(_from, _to + 1, thread_count)]
        log.debug(env_num_group_list)

        # 获取脚本列表
        model = self.listView_run_script.model()
        if model is None:
            self.show_info.create_warning_info_bar('脚本为空')
            return
        all_script_name = []
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            file_name = model.data(index, Qt.DisplayRole)
            all_script_name.append(file_name)

    def run_group_chrome(self, env_num_group_list, all_script_name):
        # 执行一组浏览器
        if len(env_num_group_list) <= 0:
            return

        run_env_list = env_num_group_list[0]
        env_num_group_list.pop(0)
        # 获取选中行的浏览器编号、相关配置，并启动浏览器
        model = self.tableView_env_config.model()
        chrome_info_dict = {}
        for index in run_env_list:
            chrome_info = ChromeInfo()
            chrome_info.env_num = int(model.data(model.index(index, db_data.DB_ENV_NUM_COL)))
            chrome_info.proxy_info = model.data(model.index(index, db_data.DB_PROXY_COL))
            chrome_info_dict[str(chrome_info.env_num)] = chrome_info
        self.start_new_chrome(chrome_info_dict)
        # 等待浏览器执行完成，开始执行下一组
        log.info('启动chrome...')
        self.thread = ChromeThread(chrome_info_dict, self.started_chrome_info_dict)
        self.thread.result_ready.connect(lambda :self.handle_chrome_started(env_num_group_list, all_script_name))
        self.thread.start()

    def handle_chrome_started(self, env_num_group_list, all_script_name):
        # 执行脚本
        for file_name in all_script_name:
            log.debug(file_name)
            file_name = file_name.replace('.py', '')
            module = importlib.import_module(f'pyqt.scripts.{file_name}')
            # 检查模块中是否存在 run_action 函数
            if hasattr(module, 'run_action'):
                run_action = getattr(module, 'run_action')
                # 调用 run_action 函数并传递 driver 参数
                run_action(self.started_chrome_info_dict['1'].driver)
                log.debug(f"成功调用 {file_name}.run_action")
            else:
                log.warning(f"模块 {file_name} 中没有 run_action 函数")



    def init_table_view(self):
        init_section.init_db_table_view_demo(self, self.tableView_env_config, db_data.DB_ENV_CONFIG_PATH,
                                             'env_config', 'env_config')

    def init_menu(self):
        # 构建本地账户表格菜单
        self.tableView_env_config.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_env_config.customContextMenuRequested.connect(self.env_config_menu)

    def env_config_menu(self, pos):
        """构建右键菜单"""
        try:
            # 创建一个右键菜单
            menu = QMenu(self)

            # 添加菜单项
            start_action = QAction('启动浏览器')
            add_action = QAction('添加浏览器')
            delete_action = QAction('删除浏览器')

            # 获取表格选定的范围
            selected_indexes = self.tableView_env_config.selectedIndexes()

            # 连接菜单项的触发信号
            start_action.triggered.connect(lambda checked: self.handle_start_action(selected_indexes))
            add_action.triggered.connect(lambda checked: handle_env_config_db.handle_add_env(self))
            delete_action.triggered.connect(lambda checked: handle_env_config_db.delete_env(self, selected_indexes))

            # 将菜单项添加到菜单
            menu.addAction(start_action)
            menu.addAction(add_action)
            menu.addAction(delete_action)

            # 在鼠标右键点击的位置显示菜单
            menu.exec_(self.tableView_env_config.viewport().mapToGlobal(pos))
        except Exception as e:
            log.error(e)

    def handle_start_action(self, selected_indexes):
        try:
            sender = self.sender()
            if sender == self.PrimaryPushButton_run_script:
                log.debug('按钮执行')
                selected_row_list = selected_indexes
            else:
                log.debug('菜单执行')
                # 获取选择的行
                selected_row_list = []
                for index in selected_indexes:
                    if index.row() not in selected_row_list:
                        selected_row_list.append(index.row())
            log.debug(selected_row_list)

            # 获取选中行的浏览器编号、相关配置，并启动浏览器
            model = self.tableView_env_config.model()
            chrome_info_dict = {}
            for index in selected_row_list:
                chrome_info = ChromeInfo()
                chrome_info.env_num = int(model.data(model.index(index, db_data.DB_ENV_NUM_COL)))
                chrome_info.proxy_info = model.data(model.index(index, db_data.DB_PROXY_COL))
                chrome_info_dict[str(chrome_info.env_num)] = chrome_info
            self.start_new_chrome(chrome_info_dict)
        except Exception as e:
            log.error(e)

    def start_new_chrome(self, chrome_info_dict: dict):
        def handle_start_chrome_result(return_chrome_info):
            env_num = return_chrome_info.env_num
            self.show_info.create_success_info_bar(f'浏览器：{return_chrome_info.env_num}已启动')
            self.started_chrome_info_dict[str(env_num)] = return_chrome_info

        log.info('启动chrome...')
        self.thread = ChromeThread(chrome_info_dict, self.started_chrome_info_dict)
        self.thread.result_ready.connect(handle_start_chrome_result)
        self.thread.start()

    def close_chrome(self, env_num: int):
        log.info('关闭chrome')
        chrome_info = self.started_chrome_info_dict[str(env_num)]
        chrome_info.driver.quit()
        if chrome_info.socks5_thread is not None:
            chrome_info.socks5_thread.close_socks5_proxy()
        self.started_chrome_info_dict.pop(str(env_num))

    def check_chrome_status(self):
        # 复制浏览器字典，避免修改原字典
        started_chrome_info_dict = self.started_chrome_info_dict.copy()
        # 后台执行状态检测和数据库更新
        self.thread = MyThread(self.check_and_change_chrome_status, started_chrome_info_dict)
        # 数据库更新后刷新界面
        self.thread.result_ready.connect(lambda : self.tableView_env_config.model().select())
        self.thread.start()

    def check_and_change_chrome_status(self, started_chrome_info_dict):
        for index, chrome_info in started_chrome_info_dict.items():
            driver = chrome_info.driver
            try:
                title = driver.title
                log.critical('浏览器状态正常')
                handle_env_config_db.set_chrome_status(self, chrome_info.env_num, '已启动')
            except:
                log.critical('浏览器已关闭')
                self.close_chrome(chrome_info.env_num)
                handle_env_config_db.set_chrome_status(self, chrome_info.env_num, '已关闭')
