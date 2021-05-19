from common import *

class ImageProcess:

  def __init__(self, hwnd):
    self.hwnd = hwnd

  def imgFindExist(self, dst_img, src_img):
    dst_img, src_img = np.asarray(dst_img), np.asarray(src_img)
    res = aircv.find_template(dst_img, src_img)
    logger.info( '图像对比结果--> %s' % res)
    return res

  def screenshot(self):
    hwnd = self.hwnd
    #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
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

class YysImageProcess(ImageProcess):

  def isBattleOver(self, dst_img, src_img, threshold=0.8 ):
    '''
    threshold: 阈值
    '''
    res = self.imgFindExist(dst_img, src_img)
    return res['confidence'] >= 0.8 if res is not None else None

  def isYuHunOver(self):
    dst_img = self.screenshot()
    src_img = Image.open('./assets/yuhun_over.png')
    dst_img.save('./assets/battle_over.png')
    # src_img.show()
    return self.isBattleOver(dst_img, src_img)

def testIsImgExist():
    a = aircv.imread('./battle_over.png')
    b = aircv.imread('./yuhun_over.png')
    logger.info(YysImageProcess(None).isBattleOver(a, b))

if __name__ == '__main__':
  testIsImgExist()
