from yys_window import YysWindow

def main():
  yysWin = YysWindow()
  yysWin.run(['yuHun'])

if __name__ == "__main__":
  # main()
  import webview
  from webview.platforms.cef import settings
  settings.update({
      'persist_session_cookies': True
  })

  window = webview.create_window(
      title='百度一下,全是广告',
      url='http://www.baidu.com',
      resizable=True,    # 固定窗口大小
      text_select=True,   # 禁止选择文字内容
      confirm_close=True,   # 关闭时提示
  )
  webview.start(debug=True, gui='cef')
  pass
