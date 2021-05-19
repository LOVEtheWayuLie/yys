import logging
import sys

__all__ = ['logger']

logger = logging.getLogger()
logLevel = logging.INFO
logger.setLevel(logLevel)

# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler()
handler.setLevel(logLevel)

# # 创建一个格式器formatter并将其添加到处理器handler
formatter = logging.Formatter("%(levelname)-5s %(asctime)s %(filename)s  %(funcName)s:%(lineno)s : %(message)s")
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)