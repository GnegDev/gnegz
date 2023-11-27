import random

class Matrix:
    def __init__(self, matrixSize):
        self.matrixSize = matrixSize

        self.score = 0
        self.winScore = 0

        self.matrix = list()
        for yWriter in range(0, matrixSize):
            templine = []
            for xWriter in range(0, matrixSize):
                if random.randint(0, 100) >= 80:
                    templine.append({"mode": "closed", "hasMine": True, "checkedScore": False, "checkedZero": False})
                else:
                    templine.append({"mode": "closed", "hasMine": False, "checkedScore": False, "checkedZero": False})
                    self.winScore += 1
            self.matrix.append(templine)

    def getCell(self, xPos, yPos):
        return self.matrix[yPos][xPos]
    
    def gainScore(self, x, y):
        if self.matrix[y][x]["checkedScore"] == False:
            self.score += 1
            self.matrix[y][x]["checkedScore"] = True
    
    def countMines(self, x, y):
        result = 0
        for yChecker in range(y - 1, y + 2):
            for xChecker in range(x - 1, x + 2):
                if yChecker >= 0 and yChecker < len(self.matrix) and xChecker >= 0 and xChecker < len(self.matrix) and self.matrix[yChecker][xChecker]["hasMine"] == True:
                    result += 1
        return result

    def revealCells(self, x, y):
        self.matrix[y][x]["checkedZero"] = True 
        for yChecker in range(y - 1, y + 2):
            for xChecker in range(x - 1, x + 2):
                if yChecker >= 0 and yChecker < len(self.matrix) and xChecker >= 0 and xChecker < len(self.matrix):
                    self.matrix[yChecker][xChecker]["mode"] = "opened"
                    self.gainScore(xChecker, yChecker)
                    if self.countMines(xChecker, yChecker) == 0 and self.matrix[yChecker][xChecker]["checkedZero"] == False:
                        self.matrix = self.revealCells(xChecker, yChecker)
        return self.matrix
    
    def revealMatrix(self):
        for yWriter in range(0, self.matrixSize):
            for xWriter in range(0, self.matrixSize):
                self.matrix[yWriter][xWriter]["mode"] = "opened"