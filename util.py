from math import hypot, sqrt
import heapq
import inspect
import sys

# define character in text file, 0: empty path, 1: wall, 2: food, 3: monster, 4: pacman
class initGame:
    def __init__(self):
        self.emptyPath = "0"
        self.wall = "1"
        self.food = "2"
        self.monster = "3"
        self.pacman = "4"

# return manhattan distance between two points xy1 and xy2
def manhattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

# return euclidearn distance between two points xy1 and xy2
def euclideanDistance(xy1, xy2):
    return hypot(xy1[0] - xy2[0], xy1[1] - xy2[1])

# return chebyshev distance between two points xy1 and xy2
def chebyshevDistance(xy1, xy2):
    dx = abs(xy1[0] - xy2[0])
    dy = abs(xy1[1] - xy2[1])
    return max(dx, dy)

# return octile distance between two points xy1 and xy2
def octileDistance(xy1, xy2):
    dx = abs(xy1[0] - xy2[0])
    dy = abs(xy1[1] - xy2[1])
    return max(dx, dy) + ((sqrt(2) - 1) * min(dx, dy))

# add element not duplicate between two list
def addElementTwoList(l1):
    l2 = []
    for i in l1:
        if i not in l2:
            l2.append(i)
    # return l2

# check if pacman win the game
def isWin():
    return "win"

# check if pacman lose the game
def isLose():
    return "lose"

# helper function for searching
class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
    def __init__(self, priorityFunction):
        self.priorityFunction = priorityFunction
        PriorityQueue.__init__(self)

    def push(self, item):
        PriorityQueue.push(self, item, self.priorityFunction(item))

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)

def pause():
    # pauses the output stream awaiting user feedback
    print("<Press enter/return to continue>")
    input() # use raw_input() for python 2.x
# helper function for searching