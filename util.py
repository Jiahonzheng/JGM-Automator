import time,json

# def load_json(file: str):
#     f=open(file,encoding='utf-8')
#     content=f.read()
#     res=json.loads(content)
#     # print(res)#打印字典
#     return(res)

# def get_upgrade_list(json_list: dict):
#     return list(zip(json_list['要升级的建筑物'], json_list['对应升级次数']))

# def clip_triangle()

def short_wait():
    time.sleep(0.2)

def mid_wait():
    time.sleep(0.5)

# 三个车厢货物的位置
GOODS_POSITIONS = { 1: (0.609,0.854),
                    2: (0.758,0.815),
                    3: (0.896,0.766)}

# 货物的那个叉叉的位置 相对位置
CROSS_POSITIONS = { 1: (0.632, 0.878),
                    2: (0.776, 0.836),
                    3: (991/1080, 1517/1920)}

# 各号建筑的位置
BUILDING_POSITIONS = {
            1: (294/1080, 1184/1920),
            2: (551/1080, 1061/1920),
            3: (807/1080, 961/1920),
            4: (275/1080, 935/1920),
            5: (535/1080, 810/1920),
            6: (799/1080, 687/1920),
            7: (304/1080, 681/1920),
            8: (541/1080, 568/1920),
            9: (787/1080, 447/1920)
        }

# if __name__ == '__main__':
#     print(get_upgrade_list(load_json('./config.json')))
    