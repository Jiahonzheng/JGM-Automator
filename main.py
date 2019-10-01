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
    }

    # 连接 adb 。
    instance = Automator('QV7039V30X', targets)

    # 启动脚本。
    instance.start()
