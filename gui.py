from tkinter import *
from MBPython.miniblink import Miniblink

def gui():
  tk=Tk()
  tk.state('zoom')#全屏
  tk.update()#更新窗口状态和信息

  mb=Miniblink.init('./cache/miniblink_x64.dll')#操作核心

  if mb == 0:
    raise BaseException('miniblink和python版本不匹配')

  wke=1(mb)#得到wke控制权
  window=wke.window#miniblink的界面容器

  webwindow=window.wkeCreateWebWindow(2, tk.winfo_id(), 0, 0, tk.winfo_width()-100, tk.winfo_height())#核心组件，大小与窗口尺寸一样
  mb.wkeLoadURLW(webwindow, 'https://www.baidu.com/')#载入百度网页
  window.wkeShowWindow(webwindow)#显示组件
  window.wkeSetDebugConfig( webwindow, 'showDevTools', 'H:/anzhuang/miniblink-20210526/front_end/inspector.html')
  #下面这行代码在单独使用miniblink时用
  # window.wkeRunMessageLoop()
  tk.mainloop()

if __name__ == "__main__":
  gui()
  pass