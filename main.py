from yys_window import YysWindow
import traceback

def main():
  try:
    yysWin = YysWindow()
    yysWin.run(['yuHun'])
  except:
    traceback.print_exc()
    print('''
    =======================================
          程序崩溃请按照提示关闭重新开启
    =======================================
    ''')
  while True:
    pass

if __name__ == "__main__":
  main()
  pass
