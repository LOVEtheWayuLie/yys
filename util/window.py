import win32gui, win32con, win32api
from util import logger
import ctypes


def decWindowEffect(func=None):
    def wrap(self, *args, **kwargs):
        self.windowReset()
        return func and func(self, *args, **kwargs)
    return wrap

class Window:
    def __init__(self, title, width, height):
        hwnd = win32gui.FindWindow(None, title)
        self.hwnd = hwnd
        self.width = width
        self.height = height
        self.widthReal = None
        self.heightReal = None

        if hwnd == 0:
            raise ValueError('未检测到-%s' % title)
        if self.isAdmin(self) is False:
            raise ('没有管理权限,无法正常使用')
        
        decWindowEffect()(self)
        # # 激活最小化的窗口
        # win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        # # 激活后再获取窗口位置信息
        # rect  = win32gui.GetWindowRect(hwnd)
        # logger.info('hwnd--> %s %s' % (hwnd, rect ))
        # win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, rect[0], rect[1], width, height, win32con.SWP_SHOWWINDOW)

    @staticmethod
    def isAdmin(cls):
        '''
        判断是否有管理员权限
        '''
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    def getWindowSize(self):
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

    def windowReset(self):
        hwnd = self.hwnd
        width = self.width
        height = self.height
        rect  = win32gui.GetWindowRect(hwnd)
        isSizeEffect = self.widthReal == self.getWindowSize()[0]
        if rect[0] < 0 or isSizeEffect is False:
            # 激活最小化的窗口
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            # 激活后再获取窗口位置信息
            rect  = win32gui.GetWindowRect(hwnd)
            logger.info('重置窗口尺寸--> %s, 真实尺寸--->%s' % ((width, height), self.getWindowSize()))
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, rect[0], rect[1], width, height, win32con.SWP_SHOWWINDOW)
            self.widthReal, self.heightReal = self.getWindowSize()

    def doClick(self, cx, cy):

        hwnd = self.hwnd

        long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
        
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下

        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起