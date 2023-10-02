import numpy as np
class Structure:
    def __init__(self, r, c):
      self.rows = r
      self.cols = c
      self.board = np.zeros((r,c))
      self.score = 0

    def operate(self,ops,game):
      if len(ops) == 0:
          return
      seps = ops.split(" ")
      for sep in seps:
        num = 1
        op = "No operation"
        if len(sep) > 1:
            rpt = ""
            i = 0
            while i < len(sep):
                if sep[i].isdigit():
                    rpt += sep[i]
                else:
                    break
                i += 1
            op = sep[i:]
            if len(rpt) > 0:
                num = int(rpt)
        else:
            op = sep[0]
        game.action(num, op)
    
    
    def inBoard(self,loc):
        return (loc[0] >= 0 and loc[1] >= 0 and loc[0] < self.rows and loc[1] < self.cols)
    def at(self,loc):
        return self.board[loc[0]][loc[1]]
    def assign(self,loc, num):
        self.board[loc[0]][loc[1]] = num

    def show(self):
        disp = "Score: "+str(self.score)+"\n"
        for i in range(self.cols):
            disp += "= "
        disp += "\n"
        for r in self.board:
            for c in r:
                if c < 1:
                  disp += "  "
                else:
                  disp += str(int(c))+" "
            disp += "\n"
        for i in range(self.cols):
            disp += "= "
        return disp
    