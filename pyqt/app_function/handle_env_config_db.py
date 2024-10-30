import sqlite3
from loguru import logger as log
from pyqt.data.app_data_define import db_data



def handle_add_env(self):
    log.info('添加环境')
    data_base = sqlite3.connect(db_data.DB_ENV_CONFIG_PATH)
    cursor = data_base.cursor()
    cursor.execute('select 编号 from env_config')
    res = cursor.fetchall()
    for i in range(1, 100):
        if (i,) not in res:
            log.debug(f'添加环境: {i}')
            cursor.execute(f'insert into env_config values({i},"","", "")')
            data_base.commit()
            break
    self.tableView_env_config.model().select()

def delete_env(self, selected_indexes):
    log.debug(selected_indexes)
    model = self.tableView_env_config.model()
    for index in selected_indexes:
        model.removeRow(index.row())
    model.select()

def set_chrome_status(self, env_num: int, status: str):
    data_base = sqlite3.connect(db_data.DB_ENV_CONFIG_PATH)
    cmd = f'update env_config set 浏览器状态 = "{status}" where 编号={env_num}'
    data_base.execute(cmd)
    data_base.commit()