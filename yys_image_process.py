from common import *
from util import *

class YysImageProcess(ImageProcess):

  def isBattleOver(self):
    src_img = Image.open('./assets/battle_over.png')
    return self.isSimilar(None, src_img)
  
  def isBattleSuccessOver(self):
    src_img = Image.open('./assets/battle_sucess_over.png')
    return self.isSimilar(None, src_img)

  def isFindTreasure(self):
    '''
    御魂结束后,有宠物会发现宝藏
    '''
    src_img = Image.open('./assets/find_treasure.png')
    isTrue = self.isSimilar(None, src_img)
    if isTrue:
      logger.info('发现宝藏')
    return isTrue

  def isTongXinZhiLan(self):
    src_img = Image.open('./assets/tong_xin_zhi_lan.png')
    return self.isSimilar(None, src_img)

  def isJoinTeam(self):
    src_img = Image.open('./assets/join_team.png')
    return self.isSimilar(None, src_img)

  def isJoinTeamAuto(self):
    '''
    接受自动组队
    '''
    src_img = Image.open('./assets/join_team_auto.png')
    return self.isSimilar(None, src_img)

  def isTeamEmpty(self):
    '''
    判断当前处于空队伍状态
    '''
    return self.isSimilar(None, Image.open('./assets/team_empty.png'))

  def isTeamExitConfirm(self):
    '''
    确认退出组队
    '''
    return self.isSimilar(None, Image.open('./assets/team_exit_confirm.png'))

  def isBattleReady(self):
    '''
    战斗准备
    '''
    src_img = Image.open('./assets/battle_ready.png')
    return self.isSimilar(None, src_img)

  def isOffLine(self):
    '''
    确认掉线
    '''
    return self.loopEqual(2, './assets/off_line%s.png')

  def isReward(self):
    '''
    悬赏封印
    '''
    return self.loopEqual(2, './assets/reward%s.png')

  def isRewardAccept(self):
    '''
    接受悬赏封印
    '''
    img_path_arr = []
    pic_count = 2
    for i in range(1, pic_count+1):
      img_path_arr.append('./assets/reward_accept%s.png' % (i if i > 1 else '', ))
    for img_path in img_path_arr:
      print(img_path)
      if self.isSimilar(None, Image.open(img_path)):
        return True
    return False
    # return self.isSimilar(None, Image.open('./assets/reward_accept.png'))

def testIsImgExist(src: str, dst: str='window_shot.png'):
    a = aircv.imread('./cache/%s' % dst)
    b = aircv.imread('./assets/%s' % src)
    pro = YysImageProcess(None)
    pro.isSimilar(a, b)
    logger.info(pro.getComparResult())

if __name__ == '__main__':
  testIsImgExist('challenge_miwen.png', dst='window_shot.png')
