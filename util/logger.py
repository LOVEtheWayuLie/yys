import logging
import sys
import time
import os

__all__ = ['logger', 'logStackInfo']

logger = logging.getLogger()
logLevel = logging.INFO
logger.setLevel(logLevel)

# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler()
handler.setLevel(logLevel)

# # 创建一个格式器formatter并将其添加到处理器handler
datefmt = "%Y-%m-%d %H:%M:%S"
format_rule = "%(levelname)-5s %(asctime)s %(filename)s  %(funcName)s:%(lineno)s : %(message)s"
formatter = logging.Formatter(format_rule, datefmt=datefmt)
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)


def logStackInfo(msg, prevNum=1):
    '''
    打印指定层调用栈信息
    '''
    frame = sys._getframe(prevNum)
    f_code = frame.f_code
    print(format_rule % {
        'levelname': 'INFO',
        'asctime':  time.strftime(datefmt, time.localtime()),
        'filename': os.path.split(f_code.co_filename)[1],
        'funcName': f_code.co_name,
        'lineno': frame.f_lineno,
        'message': msg,
    })
