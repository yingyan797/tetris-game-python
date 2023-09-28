import numpy as np
from operate import Structure

def 方块(序号):
    match 序号:
        case 0:
            return np.array([[0,0],[0,1],[0,2],[0,3]])
        case 1:
            return np.array([[0,0],[0,1],[1,0],[1,1]])
        case 2:
            return np.array([[0,1],[1,0],[1,1],[1,2]])
        case 3:
            return np.array([[0,0],[1,0],[1,1],[1,2]])
        case 4:
            return np.array([[0,2],[1,0],[1,1],[1,2]])
        case 5:
            return np.array([[0,0],[0,1],[1,1],[1,2]])
        case 6:
            return np.array([[0,1],[0,2],[1,0],[1,1]])
        case _:
            #Random shape
            一组数字 = [甲 for 甲 in range(8)]
            四个方块 = np.array([[0,1],[0,2],[1,0],[1,1]])
            for 丙 in range(4):
                序号 = int(np.random.random()*len(一组数字))
                数字 = 一组数字.pop(序号)
                甲 = int(数字 / 4)
                乙 = 数字 % 4
                四个方块[丙][0] = 甲
                四个方块[丙][1] = 乙
            return 四个方块