from common import *
from util import *
from yys_image_process import YysImageProcess

class YysWindow(Window):

    def __init__(self):
        super().__init__('阴阳师-网易游戏', 400, 225)
        self.img_process = YysImageProcess(self.hwnd)
        self.count_yuhun = 0

    def run(self, task_name_arr: list):
        img_process = self.img_process
        while True:
            with img_process:
                for task in task_name_arr:
                    if hasattr(self, task):
                        getattr(self, task)()
                    else:
                        raise ValueError('不存在任务类型---> %s ' % task)
                time.sleep(1)
                self.windowReset()

    def yuHun(self):
        img_process = self.img_process

        if img_process.isYuHunSuccessOver():
            self.doClickMatch()
        if img_process.isYuHunOver():
            self.count_yuhun += 1
            confidence = img_process.getComparResult()['confidence']
            while img_process.isYuHunOver():
                self.doClickCenter()
            logger.info('第%s轮御魂结束, 相似度: %s ' % (self.count_yuhun, confidence))
            pass
        if img_process.isFindTreasure():
            logger.info('宝藏对比结果--->', img_process.getComparResult())
            self.doClickBottomCorner()
