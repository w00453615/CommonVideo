# __init__.py 为初始入口文件,工程代码的入口文件.
import time

# 导入动作库常用函数
from ascript.android.action import click, slide, Touch, gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device
from ascript.android.ui import WebWindow
from ascript.android.system import R

from .cfg.douyin import lookDouyinGuangGaoOnes
from .cfg import kuaishou
from .cfg import kuaishoujisu
from .cfg import baidu
from .cfg import xifan
from .ui import ui
from .cfg import douyin
from .cfg import hongguo
from .util import process, register, swipeUp, swipeBackOnes

print("Hello AS!")
# 点击某个地方
# click(100,100)

# swipeUp()
# time.sleep(20)
# loginit()

register(douyin.cfg)
register(kuaishou.cfg)
register(kuaishoujisu.cfg)
# register(baidu.cfg)
# register(hongguo.cfg)
register(xifan.cfg)
# register(hongguo.cfg)

ui.show(util.procList)
# process()

# ui.main_interface()


# lookDouyinGuangGaoOnes()
# system.exit()