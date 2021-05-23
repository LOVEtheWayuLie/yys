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

  def isCreateTeam(self):
    src_img = Image.open('./assets/create_team.png')
    return self.isSimilar(None, src_img)

def testIsImgExist(src: str, dst: str='window_shot.png'):
    a = aircv.imread('./cache/%s' % dst)
    b = aircv.imread('./assets/%s' % src)
    pro = YysImageProcess(None)
    pro.isSimilar(a, b)
    logger.info(pro.getComparResult())

if __name__ == '__main__':
  testIsImgExist('create_team.png')
