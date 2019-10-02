from automator import Automator
from target import TargetType

if __name__ == '__main__':
    # 声明货物要移动到的建筑 ID 。
    targets = {
        TargetType.Chair: 1,
        TargetType.Wood: 7,
        TargetType.Bottle: 4,
        TargetType.Vegetable: 5,
        TargetType.Box: 2,
        TargetType.Food: 8
        # # TargetType.Chair: 1,
        # # TargetType.Box: 2,
        # # TargetType.Dogfood: 2,
        # # TargetType.Sofa: 3,
        # # TargetType.Plant: 3,
        # TargetType.Microphone: 4,
        # # TargetType.Shoes: 5,
        # TargetType.Chicken:6,
        # # TargetType.Bottle: 4,
        # # TargetType.Vegetable: 5,
        # # TargetType.Book: 5,
        # # TargetType.Bag: 6,
        # # TargetType.Wood: 7,
        # # TargetType.Oil: 8,
        # # # TargetType.Food: 8,
        # # TargetType.Iron: 8,
        # # TargetType.Grass:9,
        # TargetType.Tool: 8,
        # # TargetType.Quilt: 9,
        
        
        

    }

    # 连接 adb 。
    instance = Automator('CB512BC4ZL', targets)

    # 启动脚本。
    instance.start()
