from logging import log
from common import *
from util import *
from yys_image_process import YysImageProcess

class YysWindow(Window):

    def __init__(self):
        super().__init__('阴阳师-网易游戏', 400, 255)
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

    @Window.decWait
    def isWaitBattleOver(self):
        '''
        战斗结束通过需要计数.
        所以需要循环判断，确保当前画面已过去
        '''
        isTrue = self.img_process.isBattleOver()
        if isTrue:
            self.doClickCenter()
            return True
        return False

    def yuHun(self):
        img_process = self.img_process

        # if img_process.isJoinTeam():
        #     if img_process.isJoinTeamAuto():
        #         self.doClickMatch(xrange=(0.8, 0.95), yrange=(0.1, 0.9))
        #         logger.info('接受自动组队请求')
        #     elif img_process.isJoinTeam():
        #         self.doClickMatch(xrange=(0.7, 0.95), yrange=(0.1, 0.9))
        #         logger.info('接受组队请求')

        if img_process.isBattleSuccessOver():
            self.doClickMatch()

        if self.isWaitBattleOver():
            self.count_yuhun += 1
            confidence = img_process.getComparConfidence()
            logger.info('第%s轮御魂结束, 相似度: %s ' % (self.count_yuhun, confidence))

        if img_process.isTeamWait():
            if img_process.isTeamChallenge():
                self.doClickMatch(xrange=(0.5, 1), yrange=(0.5, 1))

        # if img_process.isFindTreasure():
        #     logger.info('宝藏对比结果--->', img_process.getComparResult())
        #     self.doClickBottomCorner()
