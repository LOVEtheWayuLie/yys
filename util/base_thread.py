from threading import Thread
from .logger import logger
import threading
import sys

__all__=['BaseThread', 'decThread']

class BaseThread(Thread):
    def __init__(self, fun, *args, **kwargs):
        super().__init__( name='BaseThread', daemon=True)
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self._catch = None
        self.parentThread = threading.current_thread()

    def run(self):
        try:
            self.result = self.fun(*self.args, **self.kwargs)
        except BaseException as e:
            logger.exception(e)
            self._catch and self._catch()

    def setCatch(self, func):
        self._catch = func
        return self

    @staticmethod
    def decTreadNotAliveExit(thread: Thread):
        '''
        线程退出时终止父线程
        '''
        def wrapper(func):
            def wrap(*args, **kwargs):
                if thread.isAlive() is False:
                    sys.exit(0)
                return func(*args, **kwargs)
            return wrap
        return wrapper


def decThread(func):
    '''
    定义为线程任务
    '''
    def wrap(*args, **kwargs):
        t = BaseThread(func, *args, **kwargs)
        t.start()
    return wrap