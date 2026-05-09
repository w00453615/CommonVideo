import time
from random import random, randint

from ascript.android.screen import FindImages
from ascript.android.system import R

from .douyin import lookDouyinGuangGaoOnes
from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickXY, ocrFindText, \
  ocrFind, findWaitBack, WAIT_LOW, WAIT_HIGH, swipeBackApp, extract_first_num_to_int, swipeBackOnes

def lookBaoXiang(paras, x, y):
  time.sleep(2 + random())
  x, y, text = ocrFindText("看视频最高")
  if x is not None:
    clickXY(x, y)

  lookDouyinGuangGaoOnes()


  x, y, text = ocrFindText("开心收下")
  if x is not None:
    clickXY(x, y)

  return

def lookShiPinZhuanJinBi(paras, x, y):
  clickXY(x, y)

  time.sleep(2 + random())
  x, y, text = ocrFindText("看视频再领")
  if x is not None:
    clickXY(x, y)

  lookDouyinGuangGaoOnes()


  x, y, text = ocrFindText("开心收下")
  if x is not None:
    clickXY(x, y)

  return

def jinBiPos():
  print("金币位置检测")
  # res = FindImages.find_template([R.img("抖音极速版/金币.png"), ], confidence=0.7)
  res = FindImages.find([R.img("红果/金币.png") ], confidence=0.90)
  # res = FindImages([R.rel(__file__, "res/img/红果/金币.png"), ], confidence=0.95, maxcnt=1, mode=2)
  if res:
    print("找到金币了", res)
    rect = res["rect"]

    result = [rect[0], rect[1] - 50, rect[2], rect[3] + 40]
    print(result)

    return result
  else:
    print("没找到金币")

  return [887,789,1032,932]

node = {
  # '看短剧赚金币' : [
  #   {'name':'看视频再领',"text": "看视频再领", "process": clickNodeP, "delay": 45, 'count':100},
  #   {'name':'倍速',"text": "倍速", "process": forWait, "delay": 45, 'count':100},
  #   {'name':'短视频',"text": "短视频", "process": lookShortVideo, "delay": 45, 'count':100, 'jinBiPos':'立即领取', 'regex':''},
  #   {'name':'广告',"text": "广告", "process": lookGuangGao, "delay": 45, 'count':100}
  #
  # ],
  # "赚钱" : [
  #   {'name':'赚钱',"text": "现金收益", "process": None, "delay": 0, 'count': 0}
  # ],
  "看短剧赚金币": [
        {'name':'看短剧赚金币',"ocr": "立即领取", "process": lookBaoXiang, "time": 600, "delay": 0, 'count': 0}
    ],
  "宝箱": [
        {'name':'宝箱',"ocr": "点击", "process": lookBaoXiang, "delay": 45, 'count': 0}
    ],
  "看视频": [
    {'name':'看视频',"text": "首页", "process": lookShortVideo, "delay": 0, 'count': 0, 'jinBiPos': jinBiPos, 'regex':''}
  ]
}

step = [
  {'name':'看视频', "path" : ['text:首页']},
  {'name': '看短剧赚金币', "path": ['text:赚钱']},
  {'name': '宝箱', "path": ['text:赚钱']},
  # {"start": "看短剧赚金币", 'name':'看短剧赚金币', "path" : ['text:赚钱']}
]

cfg = {
  "app" : "com.phoenix.read",
  'name':'红果',
  "step" : step,
  "node" : node
}


