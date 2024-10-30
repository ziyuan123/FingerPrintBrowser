from turtledemo.penrose import start

from PyQt5.QtCore import Qt
from loguru import logger as log

from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel



def init_db_table_view_demo(self, table_view: QTableView, db_path, db_set_name, table_name):
    """从数据库加载表格视图"""
    log.info(f'加载: {table_name}')
    db = QSqlDatabase.addDatabase('QSQLITE', db_set_name)
    db.setDatabaseName(db_path)
    if not db.open():
        print("无法打开数据库！")
        return
    # 配置模型，连接数据库
    db_model = QSqlTableModel(self, db)
    db_model.setTable(table_name)
    db_model.setEditStrategy(QSqlTableModel.OnFieldChange)
    db_model.select()

    # 表格连接模型
    table_view.setModel(db_model)  # 设置model
    table_view.setSortingEnabled(True)  # 可排序
    table_view.sortByColumn(0, Qt.AscendingOrder)
    table_view.resizeColumnsToContents()  # 自动调整列宽
    table_view.horizontalHeader().setStretchLastSection(True)  # 设置伸缩模式，使最后一列填充剩余空间


def init_table_view_demo(table_view: QTableView, title_list, datas_list, col_len_list=None, if_check=False):
    """加载不依赖数据库的表格视图"""
    model = QStandardItemModel(len(datas_list), len(title_list))  # 建立x行y列的模型

    # 设置表头、表格格式、表格模型
    model.setHorizontalHeaderLabels([''] + title_list) if if_check else model.setHorizontalHeaderLabels(title_list)
    table_view.horizontalHeader().setStretchLastSection(True)  # 设置伸缩模式，使最后一列填充剩余空间
    table_view.setModel(model)

    for row_index, datas in enumerate(datas_list):
        if if_check:
            # 第一列设置为勾选框
            check_item = QStandardItem()
            check_item.setCheckable(True)
            model.setItem(row_index, 0, check_item)
            data_move = 1
        else:
            data_move = 0

        for col_index, value in enumerate(datas):
            model.setItem(row_index, col_index + data_move, QStandardItem(str(value)))

    table_view.resizeColumnsToContents()  # 调整列宽以适应内容
    # 指定列宽
    if col_len_list is None:
        return

    col_len_list = [0] + col_len_list if if_check else col_len_list
    for i in range(len(col_len_list)):
        if col_len_list[i] == 0:
            continue
        table_view.setColumnWidth(i, col_len_list[i])  # 指定列宽
