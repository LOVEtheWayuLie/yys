from common import *
from image_process import YysImageProcess

class YysWindow(Window):

    def __init__(self):
        super().__init__('阴阳师-网易游戏', 400, 225)

    def yuHun(self):
        count = 0
        while True:
            img_process = YysImageProcess(self.hwnd)
            if img_process.isYuHunOver():
                count += 1
                logger.info('第%s轮御魂' % count)
                pass
            time.sleep(1)
            self.windowReset()
        pass