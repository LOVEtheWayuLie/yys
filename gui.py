from tkinter import *
from MBPython.miniblink import Miniblink

if __name__ == "__main__":
  tk=Tk()
  tk.state('zoom')#全屏
  tk.update()#更新窗口状态和信息

  mb=Miniblink.init('./cache/miniblink_x64.dll')#操作核心

  wke=Miniblink(mb)#得到wke控制权
  window=wke.window#miniblink的界面容器

  webwindow=window.wkeCreateWebWindow(2, tk.winfo_id(),0,0, tk.winfo_width(), tk.winfo_height())#核心组件，大小与窗口尺寸一样
  mb.wkeLoadURLW(webwindow,'https://www.baidu.com/')#载入百度网页
  window.wkeShowWindow(webwindow)#显示组件
  #下面这行代码在单独使用miniblink时用
  # window.wkeRunMessageLoop()
  tk.mainloop()
  pass