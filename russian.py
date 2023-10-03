import numpy as np
from operate import Structure
from player import Session

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
        score = ""
        i = 0
        while info[i] != '\n':
            i += 1
        i += 8
        while info[i] != '\n':
            score += info[i]
            i += 1
        self.struct.score = float(score)

        i += self.struct.cols * 2 + 2
        tl = False
        block = np.zeros((4,2))
        r = 0
        minr = 0
        minc = self.struct.cols

        for j in range(self.struct.rows):
            for k in range(self.struct.cols):
                if info[i] in "12":
                    self.struct.board[j][k] = int(info[i])
                    if info[i] == '1':
                        if not tl:
                            tl = True
                            minr = j
                        if k < minc:
                            minc = k
                        block[r][0] = j
                        block[r][1] = k
                        r += 1
                i += 2
            i += 1
        self.topleft = np.array([minr, minc])
        for j in range(len(block)):
            self.currentBlock[j] = block[j] - self.topleft
        
    
    def action(self, num, op):
        vec = np.zeros(2)
        trans = np.zeros((2,2))
        mrc = max(self.struct.cols, self.struct.rows)
        if op in ["ss","dd","aa"]:
            op = op[0]
            num = mrc + 5
        match op:
            case "w": trans = np.array([[-1,0],[0,-1]])
            case "s": vec = np.array([1,0])
            case "a": vec = np.array([0,-1])
            case "d": vec = np.array([0,1])
            case "l": trans = np.array([[0,-1],[1,0]]) 
            case "r": trans = np.array([[0,1],[-1,0]])
            case "p": 
                if self.checkShift(np.array([1,0])):
                    print("Error: Not reach the bottom, cannot procede to the next block")
                    return 
                self.switch(2)
                self.nextBlock = True
                return 
            case _: 
                print("Error: Operation not recognizable")
                return 
        
        if vec[0] != 0 or vec[1] != 0:
            i = 1
            while i <= num:
                if self.checkShift(i*vec):
                    i += 1  
                else:
                    break
           
            self.switch(0)
            self.topleft += (i-1)*vec
            self.switch(1)
        else:
            if num > mrc:
                print("Too many rotations. Capped to", mrc, "times")
                num = mrc
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
                else:
                    print("Error: Rotation not successful due to obstacle")
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
        num = 0
        fac = 1
        while i >= 0:
            line = True
            for n in self.struct.board[i]:
                if n < 2:
                    line = False
                    break
            if line:
                num += 1
                self.struct.score += fac
                fac *= 1.5
                k = i
                while k > 0:
                    self.struct.board[k] = self.struct.board[k-1]
                    k -= 1
                self.struct.board[0] = np.zeros(self.struct.cols)
            else:
                i -= 1
        if num > 0:
            print("Nice job.", num,"line(s) cleared.")

    def checkFull(self):
        if not self.checkShift(np.array([1,0])):
            for i in self.struct.board[0]:
                if i > 0:
                    self.switch(1)
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

    def play(self):
        print("Welcome to tetris game.")
        resume = input("Resume previous game? Yes (y); No (any other key) ")
        login = "y"
        if resume != "y":
            login = input("Will start new game. Login or sign up? Login (y); Sign up (any other key) ")

        pname = input("Enter user name: ")
        pe = Session.findPlayer(pname)
        if login != "y": 
            if pe != "":
                print("User name exists. Please choose another one.") 
                return
            while True:
                pwd = input("Enter password: ")
                if len(pwd) >= 4:
                    pwd2 = input("Confirm password: ")
                    if pwd == pwd2:
                        print("User registered.")
                        Session.regPlayer(pname, pwd)
                        break
                    else:
                        print("Password doesn't match. Please enter again.")
                else:
                    print("Password must be no shorter than 4 characters. Choose another one.")
        else:
            pwd = input("Enter password: ")
            if pe != "" and pe == Session.encr(pwd):
                print("Login successful.")
            else:
                print("No matching user credential.")
                return

        maxScore = 0
        while True:
            ms = input("Set your goal (can be changed every time logging in): ")
            valid = True
            for m in ms:
                if not m.isdigit():
                    valid = False
                    print("Goal score must be number. Enter again.")
                    break
            if valid:
                maxScore = float(ms)
                break
        
        tn = Session.encr(pname)
        fn = "game_history/"+tn+".txt"
        print("Game starts. Please open text file", fn, ". Enter operation after \"--\" ")

        if resume:
            self.restore(fn)
            self.nextBlock = False
        else:
            open(fn, "a").close()
            self.randomize()
            self.nextBlock = True
        
        while self.struct.score < maxScore: 
          while not self.nextBlock:
            f = open(fn, "w")
            f.write("Goal: "+str(maxScore)+"\n"+self.struct.show())
            #print(self.struct.board)
            f.close()
            ops = input("-- ")
            self.struct.operate(ops, self)
          
          self.checkLine()
          self.blockGen()
          if self.checkFull():
              gameOver = "Game over. Reached the top. Your score: "+str(self.struct.score)
              f = open(fn,"a")
              f.write(gameOver)
              print(gameOver)
              return True
        congrats = "Congratulations for achieving max score " +str(maxScore) +"; Your score: "+str(self.struct.score)
        f = open(fn,"w")
        f.write(congrats)
        print(congrats)
        return True

'''
b = np.array()
g1 = Game(20,10).restore(b, 5)
'''

g1 = Russian(20,10)
g1.play()