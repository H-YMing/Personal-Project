# _*_ coding:utf-8 _*_
'''
2048game
'''
import numpy
import random

Size = 4
Matrix = numpy.zeros([Size, Size])
Score = 0


class UpdateNew(object):
    def __init__(self, matrix):
        super(UpdateNew, self).__init__()
        self.matrix = matrix
        self.score = 0
        self.zerolist = []

    def removeZero(self, rowlist):
        while True:
            mid = rowlist[:]
            try:
                rowlist.remove(0)
                rowlist.append(0)
            except:
                pass
            if rowlist == mid:
                break
        return self.combineList(rowlist)

    def combineList(self, rowlist):
        start_num = 0
        end_num = Size-rowlist.count(0)-1
        while start_num < end_num:
            if rowlist[start_num] == rowlist[start_num+1]:
                rowlist[start_num] *= 2
                self.score += int(rowlist[start_num])
                rowlist[start_num+1:] = rowlist[start_num+2:]
                rowlist.append(0)
            start_num += 1
        return rowlist

    def toSequence(self, matrix):
        lastmatrix = matrix.copy()
        m, n = matrix.shape
        for i in range(m):
            newList = self.removeZero(list(matrix[i]))
            matrix[i] = newList
            for k in range(Size-1, Size-newList.count(0)-1, -1):
                self.zerolist.append((i, k))
        if matrix.min() == 0 and (matrix != lastmatrix).any():
            GameInit.initData(Size, matrix, self.zerolist)
        return matrix


class LeftAction(UpdateNew):
    def __init__(self, matrix):
        super(LeftAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()
        newmatrix = self.toSequence(matrix)
        return newmatrix, self.score


class RightAction(UpdateNew):
    def __init__(self, matrix):
        super(RightAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()[:, ::-1]
        newmatrix = self.toSequence(matrix)
        return newmatrix[:, ::-1], self.score


class UpAction(UpdateNew):
    def __init__(self, matrix):
        super(UpAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy().T
        newmatrix = self.toSequence(matrix)
        return newmatrix.T, self.score


class DownAction(UpdateNew):
    def __init__(self, matrix):
        super(DownAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()[::-1].T
        newmatrix = self.toSequence(matrix)
        return newmatrix.T[::-1], self.score


class GameInit(object):
    """dostring for GameInit"""
    def __init__(self):
        super(GameInit, self).__init__()

    @staticmethod
    def getRandomLocal(zerolist=None):
        if zerolist is None:
            a = random.randint(0, Size-1)
            b = random.randint(0, Size-1)
        else:
            a, b = random.sample(zerolist, 1)[0]
        return a, b

    @staticmethod
    def getNewNum():
        n = random.random()
        if n > 0.8:
            n = 4
        else:
            n = 2
        return n

    @classmethod
    def initData(cls, Size, matrix=None, zerolist=None):
        if matrix is None:
            matrix = Matrix.copy()
        a, b = cls.getRandomLocal(zerolist)
        n = cls.getNewNum()
        matrix[a][b] = n
        return matrix  # 返回初始化任意位置为2或者4的矩阵

    @staticmethod
    def keyDownPressed(keyvalue, matrix):
        if keyvalue == '1':
            return UpAction(matrix)
        elif keyvalue == '2':
            return DownAction(matrix)
        elif keyvalue == '3':
            return LeftAction(matrix)
        elif keyvalue == '4':
            return RightAction(matrix)


    @staticmethod
    def gameOver(matrix):
        testmatrix = matrix.copy()
        a, b = testmatrix.shape
        for i in range(a):
            for j in range(b-1):
                if testmatrix[i][j] == testmatrix[i][j+1]:
                    return False
        for i in range(b):
            for j in range(a-1):
                if testmatrix[j][i] == testmatrix[j+1][i]:
                    return False
        return True


def main():
    matrix = GameInit.initData(Size)
    current_score = 0
    print u"当前分数：", current_score
    print matrix
    ending = False
    while True:
        opera = input("1,2,3,4:")
        actionObject = GameInit.keyDownPressed(str(opera), matrix)
        matrix, score = actionObject.handleData()
        current_score += score
        print u"当前分数：", current_score
        print matrix
        if matrix.min() != 0:
            ending = GameInit.gameOver(matrix)
        if ending:
            print u'游戏结束！'
            break


if __name__ == '__main__':
    main()
