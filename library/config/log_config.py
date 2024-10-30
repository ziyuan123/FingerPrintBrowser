import sys
from loguru import logger as log

debug = True

def config_log():
    # 移除默认的日志处理器
    log.remove()

    # 向控制台输出 INFO 及以上等级的日志
    if debug:
        log.add(sys.stderr, level="DEBUG")
    else:
        log.add(sys.stderr, level="INFO")

    # 向文件输出 DEBUG 及以上等级的日志
    log.add("debug.log", level="DEBUG")