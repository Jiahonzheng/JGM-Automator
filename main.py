from automator import Automator
from target import TargetType

if __name__ == '__main__':
    # 升级建筑列表, 实际升级是随机从这个列表中挑一个升级
    # up_list = [(1,1),(1,1),(1,1),(4,3)] # 75%的概率1号升级1次， 25%的概率4号升级3次
    up_list = [(4,1),(6,1)] # 4号升级1次， 6号升级1次
    # 收货过滤列表
    harvest_filter = [5,6,7,8] # 只收取5,6,7,8号建筑的货物
    # 连接 adb 。
    Device1 = 'QV7039V30X'
    Device2 = 'CB512BC4ZL'
    Device1Net = '10.21.20.105'
    Device2Net = '10.21.59.70'
    MuMu = '127.0.0.1:7555'
    instance = Automator(Device1, up_list, harvest_filter)
    # 启动脚本。
    instance.start()
    # instance.start_without_train()
    
