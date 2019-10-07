from automator import Automator

if __name__ == '__main__':
    # 升级建筑列表, 实际升级是随机从这个列表中挑一个升级
    #up_list = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5)]  # 雨露均沾
    # up_list = [(1,1),(1,1),(1,1),(4,3)] # 75%的概率1号升级1次， 25%的概率4号升级3次
    up_list = [(8,1),(9,1)] # 这个号建筑升级1次， 那个号建筑升级1次
    # 收货过滤列表
    harvest_filter = [2,3,4,5,6,7,8,9] # 收取这些号建筑的货物
    # 连接 adb 。
    Device1 = 'QV7039V30X'
    Device2 = 'CB512BC4ZL'
    Device1Net = '10.21.20.105'
    Device2Net = '10.21.59.70'
    MuMu = '127.0.0.1:7555'
    instance = Automator(Device2, up_list, harvest_filter)
    # 启动脚本。
    instance.start()
    
