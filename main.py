from common import *
from image_process import YysImageProcess

def isAdmin():
  '''
  判断是否有管理员权限
  '''
  return bool(ctypes.windll.shell32.IsUserAnAdmin())

def main():
  if isAdmin() is False:
    logger.info('没有管理权限,无法正常使用')
    return
  hwnd = win32gui.FindWindow(None, '阴阳师-网易游戏')
  # 激活最小化的窗口
  win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
  # 激活后再获取窗口位置信息
  rect  = win32gui.GetWindowRect(hwnd)
  logger.info('hwnd--> %s %s' % (hwnd, rect ))
  win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, rect[0], rect[1], 400, 255, win32con.SWP_SHOWWINDOW)
  img_process = YysImageProcess(hwnd)
  print( img_process.isYuHunOver())

if __name__ == "__main__":
  main()
  pass
