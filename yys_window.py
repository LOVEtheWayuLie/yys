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

    def tempActivity(self):
        '''
        阿修罗活动
        '''
        img_process = self.img_process

        if img_process.isSimilar(None, Image.open('assets/temp_activity/challenge.png')):
            self.doClickMatch()

        if img_process.isBattleSuccessOver():
            self.doClickMatch()

        if self.isWaitBattleOver():
            self.count_yuhun += 1
            confidence = img_process.getComparConfidence()
            logger.info('第%s轮活动结束, 相似度: %s ' % (self.count_yuhun, confidence))
    
    def miWen(self):
        '''
        秘闻挑战
        '''
        img_process = self.img_process

        if img_process.isSimilar(None, Image.open('assets/challenge_miwen.png')):
            self.doClickMatch()

        if img_process.isBattleSuccessOver():
            self.doClickMatch()

        if self.isWaitBattleOver():
            self.count_yuhun += 1
            confidence = img_process.getComparConfidence()
            logger.info('第%s轮活动结束, 相似度: %s ' % (self.count_yuhun, confidence))
        
        if img_process.isReward():
            if img_process.isRewardAccept():
                logger.info('当前有一个悬赏,已接受')
                self.doClickMatch()
                
        if img_process.isBattleReady():
            self.doClickMatch()

    def yuHun(self):
        img_process = self.img_process

        if img_process.isOffLine():
            self.doClickMatch(xrange=(0.4, 0.7), yrange=(0.8, 1))
            logger.info('断线期间战斗结束')
        
        if img_process.isReward():
            logger.info('收到一个悬赏封印')
            time.sleep(5) # 等待3秒再接受悬赏,尽量只接受仅给我的悬赏
            if img_process.isRewardAccept():
                logger.info('接受悬赏, 相似度%s' % img_process.getComparConfidence())
                self.doClickMatch()

        if img_process.isJoinTeam():
            if img_process.isJoinTeamAuto():
                self.doClickMatch(xrange=(0.8, 0.95), yrange=(0.1, 0.9))
                logger.info('接受自动组队请求')
            elif img_process.isJoinTeam():
                self.doClickMatch(xrange=(0.7, 0.95), yrange=(0.1, 0.9))
                logger.info('接受组队请求' if img_process.isTongXinZhiLan() is False else '接受同心之兰')

        if self.isTeamEmptyTimeout():
            logger.info('当前处于空队伍状态')
            self.doClickAppoint((10, 18), (5, 15))

        if img_process.isTeamExitConfirm():
            logger.info('确认退出队伍')
            self.doClickMatch(xrange=(0.65, 0.95), yrange=(0.67, 0.92))

        # if img_process.isBattleReady():
        #     self.doClickMatch()
        #     logger.info('点击准备战斗')

        if img_process.isBattleSuccessOver():
            self.doClickMatch()

        if self.isWaitBattleOver():
            self.count_yuhun += 1
            confidence = img_process.getComparConfidence()
            logger.info('第%s轮御魂结束, 相似度: %s ' % (self.count_yuhun, confidence))

        if img_process.isFindTreasure():
            logger.info('宝藏对比结果--->', img_process.getComparResult())
            self.doClickBottomCorner()

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

    @Window.decTimeoutByCount(5)
    def isTeamEmptyTimeout(self):
        return self.img_process.isTeamEmpty()