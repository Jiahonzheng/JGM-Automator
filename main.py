from automator import Automator
from target import TargetType

if __name__ == '__main__':
    # 声明货物要移动到的建筑 ID 。
    targets = {
        TargetType.Box: 2,
        TargetType.Dogfood: 2,
        TargetType.Sofa: 3,
        TargetType.Plant: 1,
        TargetType.Microphone: 6,
        TargetType.Microphone2: 6,
        TargetType.Shoes: 5,
        TargetType.Chicken: 5,
        TargetType.Bottle: 4,
        TargetType.Vegetable: 5,
        TargetType.Food: 8,
        TargetType.Book: 6,
        TargetType.Bag: 6,
        TargetType.Wood: 7,
        TargetType.Oil: 8,
        TargetType.Iron: 7,
        TargetType.Iron2: 7,
        TargetType.Grass:9,
        TargetType.Tool: 8,
        TargetType.Quilt: 9,
        TargetType.Chair: 1,
        TargetType.Cotton: 8,
        TargetType.Cloth: 6
        
    }
    # 升级建筑列表
    up_list = [(2,1),(3,5)] # 2号升级1次， 3号升级5次
    # 收货过滤列表
    harvest_filter = [5,6,7,8] # 只收取5,6,7,8号建筑的货物
    # 连接 adb 。
    instance = Automator('127.0.0.1:7555', targets, up_list, harvest_filter)
    # 启动脚本。
    instance.start()
