from common import *
from image_process import YysImageProcess
from yys_window import YysWindow

def isAdmin():
  '''
  判断是否有管理员权限
  '''
  return bool(ctypes.windll.shell32.IsUserAnAdmin())

def main():
  yysWin = YysWindow()
  yysWin.yuHun()

if __name__ == "__main__":
  main()
  pass
