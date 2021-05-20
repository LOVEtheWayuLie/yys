from common import *
from util import *
from yys_image_process import YysImageProcess

class YysWindow(Window):

    def __init__(self):
        super().__init__('阴阳师-网易游戏', 400, 225)
        self.img_process = YysImageProcess()

    def yuHun(self):
        count = 0
        while True:
            img_process = self.img_process

            with img_process:
                if img_process.isYuHunSuccessOver():
                    self.doClickMatch()
                if img_process.isYuHunOver():
                    count += 1
                    confidence = img_process.getComparResult()['confidence']
                    while img_process.isYuHunOver():
                        self.doClickCenter()
                    logger.info('第%s轮御魂结束, 相似度: %s ' % (count, confidence))
                    pass
                if img_process.isFindTreasure():
                    logger.info('宝藏对比结果--->', img_process.getComparResult())
                    self.doClickBottomCorner()
                # self.doClickBottomCorner()
                time.sleep(1)
                self.windowReset()
        pass