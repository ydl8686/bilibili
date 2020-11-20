# 用来测试在某短时间内每间隔一定时间重复执行一段python代码
import time


def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec


second = sleeptime(0, 0, 1)
while True:
    time.sleep(second)
    print('do action')
