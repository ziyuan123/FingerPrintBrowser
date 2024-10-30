from loguru import logger as log
from library.globals.excel_operator import ExcelOperator
from library.globals.sql_manager import SqlManager


def create_database_from_excel(data_base: str, excel_path: str):
    excel_operator = ExcelOperator(excel_path)
    # 读取表头
    header = excel_operator.output_bluk(1, 1, 'r')
    header_cmd = []
    for index, action in enumerate(header):
        tmp = str(action).split('-')
        log.debug(tmp)
        header_name = tmp[0]
        header_type = tmp[1]
        if index == 0:
            header_cmd.append((header_name, '{} primary key'.format(header_type)))
        else:
            header_cmd.append((header_name, header_type))

    sql_manager = SqlManager(data_base)
    sql_manager.create_table('user_info', header_cmd)

def add_data_from_excel(data_base: str, excel_path: str):
    excel_operator = ExcelOperator(excel_path)
    data_len = len(excel_operator.output_bluk(2, 1, 'd'))
    sql_manager = SqlManager(data_base)

    for index in range(data_len):
        log.debug('================================')
        data = excel_operator.output_bluk(index + 2, 1, 'r')
        res = sql_manager.select('user_name', 'user_info', 'user_name="{}"'.format(data[0]))
        if len(res) == 0:
            sql_manager.add('user_info', data)
            log.debug('已添加\n\n')
        else:
            log.warning('已存在\n\n')


if __name__ == '__main__':
    # create_database_from_excel('user_info.db', 'user_info.xlsx')
    add_data_from_excel('user_info.db', 'user_info.xlsx')