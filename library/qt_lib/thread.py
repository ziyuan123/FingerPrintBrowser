import asyncio
import importlib
import time

import pproxy
from loguru import logger as log
from PyQt5.QtCore import QThread, pyqtSignal

from library.auto_web_lib.AutoWeb import AutoWeb
from pyqt.data.data_struct.data_struct import ChromeInfo


class MyThread(QThread):
    result_ready = pyqtSignal(object)  # 定义一个信号，用于发送结果

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            # 在线程中执行传入的函数
            result = self.function(*self.args, **self.kwargs)
            self.result_ready.emit(result)  # 发出结果
        except Exception as e:
            log.error(e)


class Socks5ProxyThread(QThread):
    result_ready = pyqtSignal(object)
    handler = None
    def __init__(self, chrome_info: ChromeInfo):
        super().__init__()
        self.chrome_info = chrome_info
        self.prot_start = 8080

        # 创建并设置事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def init_proxy(self):
        # 解析代理
        proxy_info_list = self.chrome_info.proxy_info.split(":")
        if len(proxy_info_list) != 4:
            log.error('代理格式错误！')
            return False
        # 完善chrome_info信息
        self.chrome_info.proxy_ip = proxy_info_list[0]
        self.chrome_info.proxy_port = proxy_info_list[1]
        self.chrome_info.proxy_user = proxy_info_list[2]
        self.chrome_info.proxy_pw = proxy_info_list[3]
        self.chrome_info.socks5_listen = f'socks5://127.0.0.1:{self.prot_start + self.chrome_info.env_num}'

        # 启动socks5代理
        server = pproxy.Server(self.chrome_info.socks5_listen)
        remote = pproxy.Connection(f'socks5://{self.chrome_info.proxy_ip}:{self.chrome_info.proxy_port}'
                                   f'#{self.chrome_info.proxy_user}:{self.chrome_info.proxy_pw}')
        args = dict(rserver=[remote], verbose=log.debug)
        self.handler = self.loop.run_until_complete(server.start_server(args))
        return self.chrome_info

    def start_socks5_proxy(self):
        try:
            log.info(f"socks5 proxy started, listen: {self.chrome_info.socks5_listen}")
            self.loop.run_forever()
        except:
            print('exit!')
            self.close_socks5_proxy()

    def close_socks5_proxy(self):
        self.handler.close()
        self.loop.call_soon_threadsafe(self.loop.stop)

    def run(self):
        self.start_socks5_proxy()


class ChromeThread(QThread):
    result_ready = pyqtSignal(object)
    action_list = []
    auto_web: AutoWeb
    socks5_thread: Socks5ProxyThread

    def __init__(self, chrome_info: ChromeInfo, started_chrome_info_dict: dict, script_list=None, account_info=None):
        super().__init__()
        self.chrome_info = chrome_info
        self.started_chrome_info_dict = started_chrome_info_dict
        self.script_list = script_list
        self.account_info = account_info

    def run(self):
        chrome_info = self.chrome_info
        env_num = chrome_info.env_num
        log.critical(chrome_info.proxy_info)
        if chrome_info.proxy_info != '':
            log.info('启动代理服务')
            # 浏览器已存在于字典，且监听端口已存在，则跳过
            if (str(env_num) in self.started_chrome_info_dict and
                    self.started_chrome_info_dict[str(env_num)].socks5_thread is not None):
                log.warning(f'监听端口：{self.chrome_info.socks5_listen}已存在，不再重复启动')
                chrome_info = self.started_chrome_info_dict[str(env_num)]
            else:
                '''由于loop会阻塞线程，因此需要单独开一个线程去进行'''
                self.socks5_thread = Socks5ProxyThread(self.chrome_info)
                chrome_info = self.socks5_thread.init_proxy()
                chrome_info.socks5_thread = self.socks5_thread
                self.socks5_thread.start()
        else:
            log.info('未配置代理，无代理启动')
        # 启动浏览器
        env_num = chrome_info.env_num
        proxy = chrome_info.socks5_listen
        self.auto_web = AutoWeb(proxy)
        self.auto_web.start_new_chrome(env_num)
        chrome_info.driver = self.auto_web.driver
        if self.script_list is not None:
            for script in self.script_list:
                log.debug(script)
                file_name = script.replace('.py', '')
                module = importlib.import_module(f'pyqt.scripts.{file_name}')
                # 检查模块中是否存在 run_action 函数
                if hasattr(module, 'run_action'):
                    run_action = getattr(module, 'run_action')
                    # 调用 run_action 函数并传递 driver 参数
                    run_action(chrome_info.driver, self.account_info)
                    log.debug(f"成功调用 {file_name}.run_action")
                else:
                    log.warning(f"模块 {file_name} 中没有 run_action 函数")
        self.result_ready.emit(chrome_info)


class CheckChromeStatus(QThread):
    status_change = pyqtSignal(tuple)
    def __init__(self, started_chrome_info_dict: dict):
        super().__init__()
        self.started_chrome_info_dict = started_chrome_info_dict

    def run(self):
        while True:
            started_chrome_info_dict = self.started_chrome_info_dict.copy()
            for index, chrome_info in started_chrome_info_dict.items():
                print('chrome status', chrome_info.chrome_status)
                driver = chrome_info.driver
                try:
                    title = driver.title
                    log.critical('浏览器状态正常')
                    if chrome_info.chrome_status is None:
                        chrome_info.chrome_status = True
                        self.status_change.emit((True, index))
                except:
                    log.critical('浏览器已关闭')
                    self.status_change.emit((False, index))
            time.sleep(5)