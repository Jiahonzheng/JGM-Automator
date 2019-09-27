from enum import Enum


class TargetType(Enum):
    """
    货物枚举类型。通过截屏制作货物图片时，请确保截屏符合实际大小。
    """
    Chair = 'targets/Chair.jpg'
    Vegetable = 'targets/Vegetable.jpg'
    Bottle = 'targets/Bottle.jpg'
    Wood = 'targets/Wood.jpg'
    Food = 'targets/Food.jpg'
    Box = 'targets/Box.jpg'
