from common import *
from util import *

class YysImageProcess(ImageProcess):

  def isYuHunOver(self):
    src_img = Image.open('./assets/yuhun_over.png')
    return self.isSimilar(None, src_img)
  
  def isYuHunSuccessOver(self):
    src_img = Image.open('./assets/yuhun_sucess_over.png')
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

def testIsImgExist():
    a = aircv.imread('./cache/window_shot.png')
    b = aircv.imread('./assets/yuhun_over.png')
    logger.info(YysImageProcess(None).isSimilar(a, b))

if __name__ == '__main__':
  testIsImgExist()
