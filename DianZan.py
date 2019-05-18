#!/usr/bin/env python
# encoding: utf-8
# coding=utf-8
from time import sleep, ctime
import threading
import os
import sys
import time
import subprocess
import re


# M 2019-05-18
# 针对于单条控制命令的终端操作 system(func_swipe,func_trap)
# 若要进行多条命令操作则可以直接move掉当前执行的函数操作 do方法中进行判断操作即可
# 本地测试设备MI9

def connectDevcie():
    # 检查设备是否连接成功，如果成功返回True，否则返回False
    try:
        # 获取设备列表信息，并用"\r\n"拆分
        deviceInfo = subprocess.check_output('adb devices').decode().split("\r\n")
        # 如果没有链接设备或者设备读取失败，第二个元素为空
        if deviceInfo[1] == '':
            return False
        else:
            return True
    except Exception as e:
        print("Device Connect Fail:", e)


def getDeviceName():
    try:
        if connectDevcie():
            # 获取设备名
            deviceInfo = subprocess.check_output('adb devices -l').decode()
            deviceName = re.findall(r'device product:dipper model:(.*) device', deviceInfo, re.S)[0]
            return deviceName
        else:
            return "Connect Fail,Please reconnect Device..."
    except Exception as e:
        print("Get Device Name:", e)


def system(func_swipe, func_trap):
    while True:
        os.system(func_trap)  # USB命令控制点击操作-->点赞操作

        sleep(1)  # 视频时间延迟5秒 如需延长或缩短时长 改变参数即可
        os.system(func_swipe)  # USB命令控制滑动操作-->上滑操作
        # os.system("adb shell input tap 999 1084")#USB命令控制手指终端
        print('Start %s! %s' % (getDeviceName(), ctime()) ) # 控制台信息输出
        sleep(3)  # 视频时间延迟5秒 如需延长或缩短时长 改变参数即可


def do(event_swipe, event_trap):
    system(event_swipe, event_trap)


if __name__ == '__main__':

    # x:540->540  y:1300->500 模拟手指滑动时长100ms
    # list = ['adb shell input swipe 540 1300 540 500 100','adb shell input tap 999 1084']#控制台命令code
    # 屏幕分辨率
    wm_size = subprocess.check_output('adb shell wm size').decode().rstrip().replace('Physical size: ', '').split('x')

    x = int(int(wm_size[0]) * 0.9305)
    y = int(int(wm_size[1]) * 0.6077)

    list = ['adb shell input swipe 540 1300 540 300 100', 'adb shell input tap {0} {1}'.format(x, y)]  # 控制台命令code

    do(list[0],list[1])


    # 主线程
    print('end:%s' % ctime())