from dataclasses import dataclass
from selenium import webdriver

@dataclass
class ChromeInfo:
    env_num: int = None

    proxy_info: str = None
    proxy_ip: str = None
    proxy_port: str = None
    proxy_user: str = None
    proxy_pw: str = None

    socks5_thread: any = None
    socks5_listen: int = None

    driver: webdriver = None
    chrome_status: bool = None