from util import logger, logStackInfo
from common import *
from .image_process import ImageProcess
from .base_thread import *


def decWindowEffect(func=None):
    def wrap(self, *args, **kwargs):
        self.windowReset()
        return func and func(self, *args, **kwargs)
    return wrap

def decSafeMonitorClick(func=None):
    '''
    Click安全监测
    如果短时间内多次触发则终止程序
    '''
    count = 0
    safe_count = 10
    cycle = 20 #扫描周期
    loca = locals()

    def safeMonitorClick():
        while True:
            time.sleep(cycle)
            if loca['count'] > safe_count:
                raise BaseException('%s 秒内点击 %s 次, 触发安全监测, 终止程序' % (cycle, loca['count']))
            loca['count'] = 0
    t = BaseThread(safeMonitorClick)
    t.setName('safeMonitorClick')
    t.start()

    @BaseThread.decTreadNotAliveExit(t)
    def wrap(self, *args, **kwargs):
        loca['count'] += 1
        return func(self, *args, **kwargs)
    return wrap

class Window:
    def __init__(self, title, width, height, img_process: ImageProcess=None):
        hwnd = win32gui.FindWindow(None, title)
        self.hwnd = hwnd
        self.width = width
        self.height = height
        self.client_width = None, 
        self.client_height = None,
        self.img_process = img_process

        if hwnd == 0:
            raise ValueError('未检测到-%s' % title)
        if self.isAdmin(self) is False:
            raise PermissionError('没有管理权限,无法正常使用')
        
        self.windowReset()

    @staticmethod
    def isAdmin(cls):
        '''
        判断是否有管理员权限
        '''
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    def getClientSize(self):
        '''
        客户区域大小
        排除非客户区域的边框,菜单栏等等
        '''
        l, t, r, b = win32gui.GetClientRect(self.hwnd)
        return r, b

    def getWindowRectSize(self):
        '''
        窗口边界大小,包含非客户区域
        '''
        l, t, r, b = win32gui.GetWindowRect(self.hwnd)
        w, h = r-l, b-t
        return w, h

    def windowReset(self):
        hwnd = self.hwnd
        width = self.width
        height = self.height
        rect  = win32gui.GetWindowRect(hwnd)
        isSizeEffect = self.client_width == self.getClientSize()[0]
        if rect[0] < 0 or isSizeEffect is False:
            # 激活最小化的窗口
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            # 激活后再获取窗口位置信息
            rect  = win32gui.GetWindowRect(hwnd)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, rect[0], rect[1], width, height, win32con.SWP_SHOWWINDOW)
            self.client_width, self.client_height = self.getClientSize()
            logger.info('重置窗口尺寸--> %s, client区域尺寸--->%s' % ((width, height), self.getClientSize()))

    @decSafeMonitorClick
    def doClick(self, cx, cy):
        '''
        点击坐标是根据Client区域范围来的
        '''
        hwnd = self.hwnd
        long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
        coor = cx, cy
        # logger.info("点击坐标 %s " % (coor,))
        logStackInfo("点击坐标 %s " % (coor,), prevNum=5)
        time.sleep(1) # 点击后休息一会儿
        return self

    def doClickMatch(self, xrange: tuple=None, yrange: tuple=None, compar_res=None):
        '''
        点击匹配位置
        range 以百分比调控点击范围
        '''
        rectangle = compar_res['rectangle'] if compar_res is not None else self.img_process.getComparResult()['rectangle']
        left, top = rectangle[0]
        right, bottom = rectangle[3]
        width, height = right-left, bottom - top
        if xrange is not None:
            left, right = int(xrange[0] * width + left), int(xrange[1] * width + left)
        if yrange is not None:
            top, bottom = int(yrange[0] * height + top), int(yrange[1] * height + top)
        coor = random.randint(left, right), random.randint(top, bottom)
        self.doClick( *coor)
        return self

    def doClickAppoint(self, xrang: tuple, yrange: tuple):
        coor = random.randint(xrang[0], xrang[1]), random.randint(yrange[0], yrange[1])
        return self.doClick(*coor)


    def doClickCenter(self):
        coor = self.getCoorCenter((0, 50))
        self.doClick( *coor)
        return self

    def doClickBottomCorner(self):
        '''
        点击贴底位置
        '''
        w, h = self.getWindowRectSize()
        coor = random.randint(50, w), random.randint(h-100, h)
        return self.doClick(*coor)

    def getCoorCenter(self, range=None):
        '''
        获取中心坐标
        '''
        l, t, r, b = win32gui.GetWindowRect(self.hwnd)
        offset = random.randint(*range) if range is not None else 0 
        coor = (r-l)//2 + offset, (b-t)//2 + offset
        return coor

    @staticmethod
    def decWait(func):
        '''
        循环等待画面结束
        '''
        def yieldFunc(self: Window, *args, **kwargs):
            while True:
                self.img_process.windowImageUpdate()
                yield func(self, *args, **kwargs)

        def wrap(self: Window, *args, **kwargs):
            if func(self, *args, **kwargs):
                compar_res = self.img_process.getComparResult()
                generate = yieldFunc(self, *args, **kwargs)
                while next(generate):
                    pass
                self.img_process.compar_res = compar_res
                return True
            return False
        return wrap

    @staticmethod
    def decTimeoutByCount(num=5):
        '''
        停留在指画面时间过长, 达到指定计数量
        '''
        def wrapper(func):
            empty_list = []
            def wrap(*args, **kwargs):
                res = func(*args, **kwargs)
                if res is True:
                    empty_list.append(res)
                else:
                    empty_list.clear()
                return empty_list.count(True) >= num
            return wrap
        return wrapper

