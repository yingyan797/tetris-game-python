import numpy as np
from operate import Structure

def block(index):
    match index:
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
            nums = [i for i in range(8)]
            bs = np.array([[0,1],[0,2],[1,0],[1,1]])
            for k in range(4):
                index = int(np.random.random()*len(nums))
                num = nums.pop(index)
                i = int(num / 4)
                j = num % 4
                bs[k][0] = i
                bs[k][1] = j
            return bs
              
class Russian:
    def __init__(self,r,c):
        self.struct = Structure(r,c)
        self.topleft = np.array([0,0])
        self.currentBlock = block(0)

    def randomize(self):
        for i in range(5, self.struct.rows):
            for j in range(self.struct.cols):
                if np.random.random() > 0.98:
                    self.struct.board[i][j] = 2

    def restore(self, fn):
        info = open(fn, "r").read()
        i = self.struct.restoreStruct(info)
        for j in range(4):
            for k in range(2):
                self.currentBlock[j][k] = int(info[i])
                i += 1
        t1 = ""
        while info[i] != '-':
            t1 += info[i]
            i += 1
        i += 1
        t2 = ""
        while i < len(info):
            t2 += info[i]
            i += 1
        self.topleft[0] = int(t1)
        self.topleft[1] = int(t2)
    
    def action(self, num, op):
        vec = np.zeros(2)
        trans = np.zeros((2,2))
        mrc = self.struct.rows
        if self.struct.cols > mrc:
            mrc = self.struct.cols
        if num > mrc:
            num = mrc
        if op in ["ss","dd","aa"]:
            op = op[0]
            num = mrc
        match op:
            case "w": trans = np.array([[-1,0],[0,-1]])
            case "s": vec = np.array([1,0])
            case "a": vec = np.array([0,-1])
            case "d": vec = np.array([0,1])
            case "l": trans = np.array([[0,-1],[1,0]]) 
            case "r": trans = np.array([[0,1],[-1,0]])
            case "p": 
                if self.checkShift(np.array([1,0])):
                    return 
                self.switch(2)
                self.nextBlock = True
                return 
            case "exit":
                self.pause = True
                return
            case _: return 
        
        if vec[0] != 0 or vec[1] != 0:
            for i in range(num):
                if self.checkShift(vec):
                    self.switch(0)
                    self.topleft += vec
                    self.switch(1)
                else:
                    return
        else:
            for j in range(num):
                nb = self.currentBlock.copy()
                left = 0
                up = 0
                for i in range(4):
                    nb[i] = np.dot(trans, self.currentBlock[i])
                    if nb[i][0] < up:
                        up = nb[i][0]
                    if nb[i][1] < left:
                        left = nb[i][1]
                for i in range(4):
                    nb[i] -= np.array([up, left])
                if self.checkRotate(nb):
                    self.switch(0)
                    self.currentBlock = nb
                    self.switch(1)
        return
    
    def checkShift(self,vec):
        for p in self.currentBlock:
            loc = self.topleft + p + vec
            if not self.struct.inBoard(loc) or self.struct.at(loc) > 1:
                return False
        return True
    
    def checkRotate(self, nb):
        for p in nb:
            loc = self.topleft + p
            if not self.struct.inBoard(loc) or self.struct.at(loc) > 1:
                return False
        return True
    
    def switch(self, on):
        for p in self.currentBlock:
            loc = self.topleft + p
            self.struct.assign(loc, on)        

    def checkLine(self):
        i = self.struct.rows - 1
        fac = 1
        while i >= 0:
            line = True
            for n in self.struct.board[i]:
                if n < 2:
                    line = False
                    break
            if line:
                self.struct.score += fac
                fac *= 1.5
                k = i
                while k > 0:
                    self.struct.board[k] = self.struct.board[k-1]
                    k -= 1
                self.struct.board[0] = np.zeros(self.struct.cols)
            else:
                i -= 1
    def checkFull(self):
        if not self.checkShift(np.array([1,0])):
            for i in self.struct.board[0]:
                if i > 0:
                    return True
        return False

    def blockGen(self):
        i = int(np.random.random()*9)
        c = int(np.random.random()*(self.struct.cols-3))
        self.currentBlock = block(i)
        self.topleft[0] = 0
        self.topleft[1] = c
        self.switch(1)
        self.nextBlock = False        

    def play(self, maxScore, resume, name):
        fn = name+".txt"
        self.pause = False
        if resume:
            self.nextBlock = False
            self.restore(fn)
        else:
          self.nextBlock = True
          self.randomize()
        while self.struct.score < maxScore: 
          while not self.nextBlock and not self.pause:
            f = open(fn, "w")
            f.write("Goal: "+str(maxScore)+"\n"+self.struct.show())
            #print(self.struct.board)
            f.close()
            ops = input("请输入操作：")
            self.struct.operate(ops, self)
          if self.pause:
              break
          self.checkLine()
          self.blockGen()
          if self.checkFull():
              f = open(fn,"a")
              f.write("Game over. Reached the top. Your score: "+str(self.struct.score))
              return True
        f = open(fn,"w")
        if self.pause:
            print(self.struct.board)
            self.struct.writeStruct(f)
            for r in self.currentBlock:
                for c in r:
                  f.write(str(int(c)))
            f.write(str(int(self.topleft[0])) +"-"+ str(int(self.topleft[1])))
            return False
        f.write("Congratulations for achieving max score " +str(maxScore) +"; Your score: "+str(self.struct.score))
        return True

'''
b = np.array()
g1 = Game(20,10).restore(b, 5)
'''

g1 = Russian(20,10)
g1.play(10, False, "zubair")