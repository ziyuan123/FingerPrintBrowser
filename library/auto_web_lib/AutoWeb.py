import time, os
from loguru import logger as log
from library.auto_web_lib import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class AutoWeb:
    driver: webdriver.Chrome = None

    def __init__(self, proxy=None):
        # 1. 指定chrome、chromedriver路径
        self.options = webdriver.ChromeOptions()  # 创建ChromeOptions对象
        self.options.binary_location = config.chrome_path  # 指定Chrome路径
        self.service = Service(executable_path=config.chrome_driver_path)  # 创建Service对象，指定ChromeDriver路径

        # 2. 配置浏览器
        # 指定用户数据目录
        self.user_env_root_path = config.user_env_root_path
        # 3. 代理配置
        if proxy is not None:
            log.debug('配置代理: {}', proxy)
            self.options.add_argument('--proxy-server=' + proxy)
            # self.options.add_argument('--proxy-server=http://localhost:7890')
        else:
            log.debug('未配置代理')

    def start_new_chrome(self, env_num):
        """
        启动新的chrome浏览器
        """
        try:
            log.info('1. 配置环境路径')
            env_path = os.path.join(self.user_env_root_path, f'env{env_num}')
            user_env_path = os.path.abspath(env_path)

            log.info(f'    路径{user_env_path}是否存在：{os.path.exists(user_env_path)}')
            user_env_setting = f"--user-data-dir={user_env_path}"
            self.options.add_argument(user_env_setting)

            log.info('2. 启动浏览器：{}', env_num)
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            log.debug('浏览器[{}]已启动', env_num)
            return True
        except Exception as e:
            log.error(f'启动浏览器{env_num}启动失败，请确认该浏览器是否已开启。\n错误信息：\n{e}')
            return False


if __name__ == '__main__':
    auto_web = AutoWeb()
    auto_web.start_new_chrome(1)