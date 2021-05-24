from .logger import logger
from common import *
from ctypes import windll

class ImageProcess:
  '''
  为了方便实现状态机
  window_image 每次with进入时更新截图
  compar_res 每次图片对比更新对比结果
  '''

  def __init__(self, hwnd):
    self.hwnd = hwnd
    self.compar_res = None
    self.window_image = None

  def __enter__(self):
    self.window_image = self.windowShot()
    self.saveImage(self.window_image, './cache/window_shot.png')
    return self

  def __exit__(self, exc_type, exc_value, exc_tb):
    if exc_tb is not None:
      logger.error('异常: %s' % exc_tb)
    self.window_image = None

  def imgFindExist(self, dst_img, src_img):
    '''
    每次对比更新对比结果
    '''
    dst_img, src_img = np.asarray(dst_img), np.asarray(src_img)
    res = aircv.find_template(dst_img, src_img)
    # logger.info( '图像对比结果--> %s' % res)
    self.compar_res = res
    return res

  def getComparResult(self) -> dict:
    return self.compar_res

  def getComparConfidence(self) -> float:
    return self.compar_res and self.compar_res['confidence']

  def printComparResult(self):
    logger.info( '图像对比结果--> %s' % self.getComparResult())

  def isSimilar(self, dst_img, src_img, threshold=0.9 ) -> bool:
    '''
    threshold: 阈值
    '''
    if dst_img is None:
      dst_img = self.window_image
    res = self.imgFindExist(dst_img, src_img)
    return res['confidence'] >= 0.8 if res is not None else False

  def windowShot(self, isOnlyClient=True):
    '''
    默认只截取客户区域
    '''
    hwnd = self.hwnd
    #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetClientRect(hwnd) if isOnlyClient else win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hwnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    windll.user32.PrintWindow(hwnd,saveDC.GetSafeHdc(), 1 if isOnlyClient else 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)

    #内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)

    return im_PIL

  def saveImage(self, img, path):
    dirname = os.path.dirname(path)
    if os.path.exists(dirname) is False:
      os.makedirs(dirname)
    img.save(path)