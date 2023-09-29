import numpy as np
from operate import Structure

def 坐标集合(一组坐标):
     return np.array(一组坐标)

def 随机生成(最大值):
    return 变成整数(np.random.random()*最大值)

def 范围(最大值):
    return range(最大值)

def 长度(数组):
    return len(数组)

def 变成整数(n):
    return int(n)

def 数组取元素于位置并删除(数组, 位置):
    return 数组.pop(位置)

def 方块(序号):
    match 序号:
        case 0:
            return 坐标集合([[0,0],[0,1],[0,2],[0,3]])
        case 1:
            return 坐标集合([[0,0],[0,1],[1,0],[1,1]])
        case 2:
            return 坐标集合([[0,1],[1,0],[1,1],[1,2]])
        case 3:
            return 坐标集合([[0,0],[1,0],[1,1],[1,2]])
        case 4:
            return 坐标集合([[0,2],[1,0],[1,1],[1,2]])
        case 5:
            return 坐标集合([[0,0],[0,1],[1,1],[1,2]])
        case 6:
            return 坐标集合([[0,1],[0,2],[1,0],[1,1]])
        case _:
            #Random shape
            一组数字 = [甲 for 甲 in 范围(8)]
            四个方块 = 坐标集合([[0,1],[0,2],[1,0],[1,1]])
            for 丙 in 范围(4):
                序号 = 随机生成(长度(一组数字))
                数字 = 数组取元素于位置并删除(一组数字,序号)
                甲 = 变成整数(数字 / 4)
                乙 = 数字 % 4
                四个方块[丙][0] = 甲
                四个方块[丙][1] = 乙
            return 四个方块
        
print(方块(5))