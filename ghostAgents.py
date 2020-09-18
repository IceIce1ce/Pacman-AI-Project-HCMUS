import util
from setup_map import *
from copy import deepcopy
from random import randint

class GhostRules:
    # init for ghost agent
    def __init__(self, location, view, mapResolution, level):
        self.location = location # current position of monster
        self.view = view # view of monster and pacman take by fixed number (diameter with pacman/ghost position in center) for calculating 8 tiles x 3
        self.actions = ["up", "down", "left", "right", "stop"] # list valid actions of monster
        self.InitMap = initGame()
        self.myInitMap = self.InitMap.monster
        self.map = Map(mapResolution[0], mapResolution[1]) # get resolution of map for calculating 8 tiles x 3
        self.level = level # level 3: ramdom move ghost, level 4: seek and kill pacman

    # remove actions which not exists in actions state provided to avoid monster go out of map
    def getDistribution(self, direction):
        try: self.actions.remove(direction)
        except ValueError: print("Sorry, current action of monster is not exists in valid actions")

    # returns a counter encoding a distribution over actions from the provided state
    def getDistributionAction(self, state):
        util.raiseNotDefined()

    # check if position of monsters is out of bound
    def checkValidGhostPosition(self):
        x_monster, y_monster = self.location[0], self.location[1]
        if (x_monster >= self.map.width or x_monster < 0) or (y_monster >= self.map.height or y_monster < 0): return False
        return True

    # direction for ghost, each step pacman move, each step ghost move
    def move(self, mapGame):
        legalMove = [] # if list bestMove is legal, add those actions to list legalMove
        bestMove = [] # list store optimize action for ghost to seek and kill pacman in 8 tiles x 3
        # if level game is 1, 2, just update fixed positions in map
        if self.level < 3:
            mapGame.update(self.location, self.location, self.myInitMap)
            return
        # if level 3: random move ghost, level 4, ghost will find position of pacman in 8 tiles x 3, then move to that position to kill pacman
        if self.level == 4: bestMove = deepcopy(self.seek_pacman(mapGame)) # copy possible actions from function seek_pacman then check its validity
        # check if action of monster is an valid action
        for i in bestMove:
            if i in self.actions:
                legalMove.append(i) # if that action is legal, add it to list legalMove
        # if legalMove is empty, copy actions from random actions
        if len(legalMove) == 0: legalMove = deepcopy(self.actions)
        directionGhost = self.random_move(legalMove) # random action of ghost and check if action is legal to avoid ghost go out of bound
        x_monster, y_monster = self.location[0], self.location[1] # get current position of ghost
        # if go up, keep x-coordinate and decrease y-coordinate
        if directionGhost == "up":
            mapGame.update(self.location, [x_monster, y_monster - 1], self.myInitMap) # update new state of map after ghost moving up 1 step
            self.update([x_monster, y_monster - 1]) # update new location of ghost from its predecessor
            return
        # if go down, keep x-coordinate and increase y-coordinate
        if directionGhost == "down":
            mapGame.update(self.location, [x_monster, y_monster + 1], self.myInitMap) # update new state of map after ghost moving down 1 step
            self.update([x_monster, y_monster + 1]) # update new location of ghost from its predecessor
            return
        # if go left, decrease x-coordinate and keep y-coordinate
        if directionGhost == "left":
            mapGame.update(self.location, [x_monster - 1, y_monster], self.myInitMap) # update new state of map after ghost moving left 1 step
            self.update([x_monster - 1, y_monster]) # update new location of ghost from its predecessor
            return
        # if go right, increase x-coordinate and keep y-coordinate
        if directionGhost == "right":
            mapGame.update(self.location, [x_monster + 1, y_monster], self.myInitMap) # update new state of map after ghost moving right 1 step
            self.update([x_monster + 1, y_monster]) # update new location of ghost from its predecessor
            return
        # if ghost want to stop at fixed position and don't want to move at next step
        if directionGhost == "stop":
            mapGame.update(self.location, self.location, self.myInitMap)
            return

    # random move ghost instead of stopping at a fixed position
    def random_move(self, move):
        # in case ghost just have one possible path to move
        if len(move) == 1: return move[0]
        # if ghost have no possible path to move
        # elif len(move) == 0: return None
        # avoid ghost just stop at a fixed position and don't want to move if ghost have another possible action beside stop action
        try: self.getDistribution("stop")
        except: pass
        return move[randint(0, len(move) - 1)] # after add action to list legalAction, random list legalAction and check it action can excute, if not random to another action

    # update info new location of monster after moving to that position
    def update(self, new_location):
        self.location = deepcopy(new_location)

    # get position of pacman for monster seek and kill
    def seek_pacman(self, mapGame):
        pacman_position = deepcopy(self.scan_pacman(mapGame)) # scan for pacman position in map, if 8 tiles x 3 have pacman, copy that position
        # if pacman is out of view and monster can't see that position
        if len(pacman_position) == 0: return []
        x_pacman, y_pacman = pacman_position[0], pacman_position[1] # get pacman current position
        bestMove = [] # empty list best actions of monster
        # if x-coordinate position of monster is right direction of pacman, make monster go left
        if self.location[0] > x_pacman: bestMove.append("left")
        # if x-coordinate position of monster is left direction of pacman, make monster go right
        if self.location[0] < x_pacman: bestMove.append("right")
        # if y-coordinate position of monster is down direction of pacman, make monster go up
        if self.location[1] > y_pacman: bestMove.append("up")
        # if y-coordinate position of monster is up direction of pacman, make monster go down
        if self.location[1] < y_pacman: bestMove.append("down")
        return bestMove # return list best actions of monster

    # scan if pacman position is in 8 tiles x 3 which in view of monster
    def scan_pacman(self, mapGame):
        centerLine = int(self.view / 2) # centerLine = diameter / 2 = 5 / 2 = 2
        # init position of pacman is: (5, 4)
        # step = 1, x = (5 - 2, 5 + 2 + 1) = (3, 8) -> need 5 step from left to right with pacman in center of a circle
        for x in range(self.location[0] - centerLine, self.location[0] + centerLine + 1, 1):
            # step = 1, y = (4 - 2, 4 + 2 + 1) = (2, 7) -> need 5 step from up to down with pacman in center of a circle
            for y in range(self.location[1] - centerLine, self.location[1] + centerLine + 1, 1):
                # in case x-coordinate or y-coordinate of monster is out corner of map in 8 tiles x 3, ignore cells that are out of bound
                if (x < 0 or x >= self.map.width) or (y < 0 or y >= self.map.height): continue
                # if 8 tiles x 3 from map have pacman, get pacman position in map for monster seek and kill pacman
                if self.InitMap.pacman in mapGame.data[y][x]: return [x, y]
        return [] # return none position if pacman is out of 8 tiles x 3