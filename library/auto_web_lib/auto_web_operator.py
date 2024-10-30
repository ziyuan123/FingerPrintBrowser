import time
from loguru import logger as log

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class AutoWebOperator:
    driver: webdriver.Chrome
    window_list = []

    def __init__(self, driver):
        self.driver = driver

        self.fresh_window_list()

    def fresh_window_list(self):
        # 获取所有窗口句柄
        window_handles = self.driver.window_handles
        # 更新窗口列表
        for index, window_handle in enumerate(window_handles):
            window_handle_info = {
                'num': index,
                'handle': window_handle
            }
            self.window_list.append(window_handle_info)

    def new_window(self, name: str):
        """ 新建空白窗口 """
        js = "window.open('', '_blank');"
        self.driver.execute_script(js)
        self.fresh_window_list()

    def clean_cookie(self, times=2):
        url = 'chrome://settings/clearBrowserData'
        self.driver.switch_to.window(self.window_list[0]['handle'])

        for i in range(times):
            try:
                self.driver.get(url)
                time.sleep(1)

                def expand_shadow_element(element):
                    shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
                    log.info(shadow_root)
                    return shadow_root

                # dialog
                outer = expand_shadow_element(self.driver.find_element(by="css selector", value="body > settings-ui"))
                outer_2 = expand_shadow_element(outer.find_element(by="css selector", value="#main"))
                outer_3 = expand_shadow_element(outer_2.find_element(by="css selector", value="settings-basic-page"))
                outer_4 = expand_shadow_element(
                    outer_3.find_element(by="css selector",
                                         value="#basicPage > settings-section:nth-child(10) > settings-privacy-page")
                )
                outer_5 = expand_shadow_element(outer_4.find_element(by="css selector",
                                                                     value="settings-clear-browsing-data-dialog"))

                inner = outer_5.find_element(by="css selector", value="#clearBrowsingDataConfirm")
                inner.click()
                time.sleep(2)
                return True
            except:
                log.error("未找到清除缓存按钮")

        return False

    def get_element(self, _elem: str, _time_out=3, by=By.XPATH):
        """
        等待获取指定元素
        :param _elem: 元素标签
        :param by: [可选] 元素判断方式
        :param _time_out: [可选] 超时，默认3
        :return: 元素对象/False
        """
        for i in range(_time_out):
            try:
                elem = self.driver.find_element(by=by, value=_elem)
                if elem:
                    return elem
                else:
                    log.warning('重试[{}]，暂未发现对象', i)
                    time.sleep(1)
                    continue
            except:
                time.sleep(1)
                log.warning('重试[{}]，寻找元素错误', i)
                continue

        log.warning("找寻对象超时！")
        return False

    def wait_find_xpath(self, _elem: str, name='', _time_out=5, by=By.XPATH, if_warning=True):
        """
        等待指定元素
        :param _elem:
        :param by: [可选] 元素判断方式
        :param _time_out: [可选] 超时，默认2
        :param name: [可选] 检测元素名称，默认不检测
        :param if_warning: [可选]
        :return: 元素对象 or F
        """
        for i in range(_time_out):
            try:
                self.driver.implicitly_wait(1)
                elem = self.driver.find_element(by=by, value=_elem)
                if elem:
                    pass
                    # log.debug("找到对象！")
                else:
                    log.warning('暂未发现对象，当前第{}次找寻', i)
                    time.sleep(1)
                    continue
                if name != '':
                    if not self.check_elem_name(_elem, name, by=by, if_warning=if_warning):
                        time.sleep(1)
                        continue
                return elem
            except:
                time.sleep(1)
                log.warning('暂未发现对象，当前第{}次找寻', i)
                continue

        log.warning("找寻对象超时！")
        return False
    def check_elem_name(self, xpath: str, name: str, by=By.XPATH, if_warning=True):
        """
        检测元素名称
        :param xpath:
        :param name:
        :param by:
        :param if_warning:
        :return:  T or F
        """
        try:
            elem = self.driver.find_element(by=by, value=xpath)
            if name in elem.text:
                log.debug('元素名称正确，元素名称[{}]', elem.text)
                return True
            else:
                if if_warning:
                    log.warning('元素名称错误，目标名称[{}]，实际名称[{}]', name, elem.text)
                return False
        except:
            log.warning('未找到指定元素！')
            return False

    @staticmethod
    def wait_element_enable(element: WebElement, _time_out=3):
        """
        等待按钮可用； 注意！部分网站未加载好的时候，交易按钮是可用的！ 需要页面加载好之后，按钮才开始显示disable！
        :param element: 网页元素
        :param _time_out: 超时，默认3秒
        :return:  T or F
        """
        for i in range(_time_out):
            try:
                elem = element
                if elem.is_enabled():
                    log.debug("按钮可用！")
                    return elem
                elif not elem.is_enabled():
                    log.warning('重试[{}]，按钮暂不可用', i)
                    time.sleep(1)
                    continue
            except:
                time.sleep(1)
                log.warning('重试[{}]，元素is_enabled对象错误', i)
                continue
        log.error('等待按钮enable超时！')
        return False

    @staticmethod
    def get_input_text(element: WebElement):
        try:
            value = element.get_attribute("value")
            return str(value)
        except Exception as e:
            log.warning('未获取到输入框内容\n{}', e)
            return False
