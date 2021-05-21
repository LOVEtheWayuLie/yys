from util import logger
from common import *
from .image_process import ImageProcess


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
    cycle = 20
    loca = locals()

    def asyncTask():
        time.sleep(cycle)
        if loca['count'] > safe_count:
            logger.error('%s 秒内点击 %s 次, 触发安全监测, 终止程序' % (cycle, loca['count']))
            sys.exit(0)
        loca['count'] = 0
        asyncTask()
    thread = Thread(target=asyncTask)
    thread.start()

    def wrap(self, *args, **kwargs):
        if thread.isAlive() is False:
            sys.exit(0)
        loca['count'] += 1
        return func(self, *args, **kwargs)
    return wrap

class Window:
    def __init__(self, title, width, height, img_process: ImageProcess=None):
        hwnd = win32gui.FindWindow(None, title)
        self.hwnd = hwnd
        self.width = width
        self.height = height
        self.widthReal = None
        self.heightReal = None
        self.img_process = img_process

        if hwnd == 0:
            raise ValueError('未检测到-%s' % title)
        if self.isAdmin(self) is False:
            raise ('没有管理权限,无法正常使用')
        
        self.windowReset()

    @staticmethod
    def isAdmin(cls):
        '''
        判断是否有管理员权限
        '''
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    def getWindowRealSize(self):
        '''
        获取真实窗口大小
        '''
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.hwnd),
            ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect)
            )
            size = (rect.right - rect.left, rect.bottom - rect.top)        
            return size
    
    def getWindowRectSize(self):
        '''
        窗口边界大小
        '''
        l, t, r, b = win32gui.GetWindowRect(self.hwnd)
        w, h = r-l, b-t
        return w, h

    def windowReset(self):
        hwnd = self.hwnd
        width = self.width
        height = self.height
        rect  = win32gui.GetWindowRect(hwnd)
        isSizeEffect = self.widthReal == self.getWindowRealSize()[0]
        if rect[0] < 0 or isSizeEffect is False:
            # 激活最小化的窗口
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            # 激活后再获取窗口位置信息
            rect  = win32gui.GetWindowRect(hwnd)
            logger.info('重置窗口尺寸--> %s, 真实尺寸--->%s' % ((width, height), self.getWindowRealSize()))
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, rect[0], rect[1], width, height, win32con.SWP_SHOWWINDOW)
            self.widthReal, self.heightReal = self.getWindowRealSize()

    @decSafeMonitorClick
    def doClick(self, cx, cy):

        hwnd = self.hwnd
        long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
        coor = cx, cy
        logger.info("点击坐标 %s " % (coor,))
        time.sleep(1) # 点击后休息一会儿
        return self

    def doClickMatch(self):
        '''
        点击匹配位置
        '''
        rectangle = self.img_process.getComparResult()['rectangle']
        left, top = rectangle[0]
        right, bottom = rectangle[3]
        coor = random.randint(left, right), random.randint(top, bottom)
        self.doClick( *coor)
        return self


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
