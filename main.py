from automator import Automator
import subprocess
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    # 升级建筑列表, 实际升级是随机从这个列表中挑一个升级, 为空不升级
    up_list = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5)]  # 雨露均沾
    # up_list = [(1,1),(1,1),(1,1),(4,3)] # 75%的概率1号升级1次， 25%的概率4号升级3次
    up_list = [(4,1),(9,1)] # 这个号建筑升级1次， 那个号建筑升级1次
    # 收货过滤列表
    harvest_filter = [5,8] # 收取这些号建筑的货物
    # adb设备列表
    Device1 = 'QV7039V30X'
    Device2 = 'CB512BC4ZL'
    Device1Net = '192.168.2.9'
    Device2Net = '10.21.59.70'
    MuMu = 'emulator-5554'

    policy = True # 是否自动升级政策
    task = True # 是否自动完成任务
    goods = True # 是否扫货
    speed_up = True # 是否自动重启加速刷火车
    # if b'connected' in subprocess.check_output('adb connect '+ MuMu):
        # print("Successfully connected to MuMu.")
    auto_red_bag = ['small', 'middle']
    instance = Automator(Device1Net, up_list, harvest_filter,auto_policy=policy,auto_task=task, auto_goods = goods, speedup=speed_up, auto_red_bag=auto_red_bag)
    # 启动脚本。
    instance.start()
    
