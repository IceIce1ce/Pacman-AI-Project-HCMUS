from setup_map import *
from random import randint
import util

class PacmanRules:
    def __init__(self, location, view, mapResolution, food, level):
        self.location = location # current location of pacman
        self.food = food # keep total food that map provided
        self.food_count = food # count food pacman had seen in map, each food pacman eat, decrease this value and if food <= 0, pacman win the game
        self.food_position = []  # list store positions of food pacman need to eat which pacman detect during scanning
        self.view = view # view of monster and pacman take by fixed number (diameter with pacman/ghost position in center) for calculating 8 tiles x 3
        self.level = level # level of game
        self.map = Map(mapResolution[0], mapResolution[1]) # pacman don't know the world, so create a map specific for pacman to decide which path is best move for pacman go to food and avoid going out of bound
        self.actions = ["up", "down", "left", "right", "stop"] # list valid actions of pacman
        self.InitMap = initGame()
        self.myInitMap = self.InitMap.pacman
        self.goal_state = self.create_important_positions() # assume we have board 5x5, we will create 4 position (2,2), (2,4), (4,2), (4,4) which pacman'll try to reach these position for scanning area around
        self.map_scanned = False # check whether pacman scan all about map, if pacman scaned and know all about map, this will be True
        self.previous_location = [] # list store all locations pacman went through to make pacman avoid duplicate path which try to make pacman go another path and scan full view of map as much as possible
        self.godEye = False # let pacman know all position of food when pacman scanned and have full view of map or provide full view of map when level of pacman is 1 and 2

    # update info new location of pacman after moving to that position
    def update(self, new_location):
        self.location = deepcopy(new_location)

    # remove actions which not exists in actions state provided to avoid pacman go out of map
    def getDistribution(self, direction):
        try: self.actions.remove(direction)
        except ValueError: print("Sorry, current action is not exists in valid actions")

    # scan heuristic manhattan distance to know whether monsters have around of pacman to help pacman avoid dangerous location
    def scan_monster_stay_near(self, mapGame):
        blueZone = self.calculate_manhattan_distance(mapGame) # get heuristic 8 tiles x 3 with distance < 3 of pacman
        monster_location = [] # list store position of monster in 8 tiles x 3
        for blue in blueZone:
            x_monster, y_monster = blue[0], blue[1] # get position of monster
            # if have monster in 8 tiles x 3
            if self.InitMap.monster in mapGame.data[y_monster][x_monster]: monster_location.append(blue) # add position of monsters to list to help pacman avoid dangerous positions
        return monster_location # return list positions pacman appear in 8 tiles x 3

    # help pacman avoid monster if monster appear in 8 tiles x 3
    def avoid_monster(self, monsters):
        for monster in monsters:
            # if direction of pacman is right which monster appear in left, remove action go left
            if monster[0] < self.location[0]: self.getDistribution("left")
            # if direction of pacman is left which monster appear in right, remove action go right
            if monster[0] > self.location[0]: self.getDistribution("right")
            # if direction of pacman is up which monster appear in down, remove action go down
            if monster[1] > self.location[1]: self.getDistribution("down")
            # if direction of pacman is down which monster appear in up, remove action go up
            if monster[1] < self.location[1]: self.getDistribution("up")

    # check if position of pacman is out of bound
    def checkValidPacmanPosition(self):
        x_pacman, y_pacman = self.location[0], self.location[1]
        if (x_pacman >= self.map.width or x_pacman < 0) or (y_pacman >= self.map.height or y_pacman < 0): return False
        return True

    # priority to escape monsters first, then eat food later
    def move(self, mapGame):
        self.scan_positions_around_important_positions() # remove current position from any positions around important positions after visiting
        # if level is 1 or 2 and pacman didn't scanned all view of map, give pacman full view of map for food positions
        if self.level < 3 and self.godEye == False: self.fullViewOfMap(mapGame)
        # if level is 3 or 4, use same heuristic manhattan distance in level 3 for scan monster stay near pacman
        if self.level >= 3: blueZoneMonster = self.scan_monster_stay_near(mapGame)
        bestMove = self.food_best_move() # get best move for pacman utilize food nearest
        legalMove = [] # list store valid action pacman can go
        # if level is 3 or 4 and have monster near, priority to avoid monster first
        if self.level >= 3:
            if len(blueZoneMonster) != 0:
                self.avoid_monster(blueZoneMonster) # if there is no possible valid action left, pacman can stop at current position until next step
        # if pacman didn't scanned fully map and still have food pacman didn't scan for its location
        # after scanning fully important positions, still have food pacman didn't see, continue to check collision positions because maybe in this area exists food around
        if self.map_scanned == False or self.food_count > 0:
            self.check_important_positions_collision_walls()
        for best in bestMove:
            if best in self.actions:
                legalMove.append(best) # add best move to valid action
        # if legalMove is empty, copy actions from random actions
        if len(legalMove) == 0: legalMove = deepcopy(self.actions)
        direction = self.random_move(legalMove) # try to random other actions if pacman have multi direction to move instead of stopping at current position
        self.previous_location = deepcopy(self.location) # copy current location to list previous_location to avoid pacman go a position twice
        x_pacman, y_pacman = self.location[0], self.location[1] # get pacman current position
        if direction == "left":
            mapGame.update(self.location, [x_pacman - 1, y_pacman], self.InitMap.pacman) # update new state of map after pacman moving up 1 step
            self.update([x_pacman - 1, y_pacman]) # update new location of monster from its predecessor
            return
        if direction == "right":
            mapGame.update(self.location, [x_pacman + 1, y_pacman], self.InitMap.pacman) # update new state of map after pacman moving up 1 step
            self.update([x_pacman + 1, y_pacman]) # update new location of monster from its predecessor
            return
        if direction == "up":
            mapGame.update(self.location, [x_pacman, y_pacman - 1], self.InitMap.pacman) # update new state of map after pacman moving up 1 step
            self.update([x_pacman, y_pacman - 1]) # update new location of monster from its predecessor
            return
        if direction == "down":
            mapGame.update(self.location, [x_pacman, y_pacman + 1], self.InitMap.pacman) # update new state of map after pacman moving up 1 step
            self.update([x_pacman, y_pacman + 1]) # update new location of monster from its predecessor
            return
        # if monster want to stop at fixed position and don't want to move at next step
        if direction == "stop":
            mapGame.update(self.location, self.location, self.InitMap.pacman)
            return

    # calculate manhattan distance to know whether monster or food positions is in 8 tiles x 3 which in view of pacman
    def calculate_manhattan_distance(self, mapGame):
        centerLine = int(self.view / 2) # centerLine = diameter / 2 = 5 / 2 = 2
        tiles = []  # list store new food scan which pacman detected in 8 tiles x 3
        # init position of pacman is: (5, 4)
        # step = 1, x = (5 - 2, 5 + 2 + 1) = (3, 8) -> need 5 step from left to right with pacman in center of a circle
        for x in range(self.location[0] - centerLine, self.location[0] + centerLine + 1, 1):
            # step = 1, y = (4 - 2, 4 + 2 + 1) = (2, 7) -> need 5 step from up to down with pacman in center of a circle
            for y in range(self.location[1] - centerLine, self.location[1] + centerLine + 1, 1):
                # in case x-coordinate or y-coordinate of pacman is corner of map in 8 tiles x 3, ignore location of 8 tiles x 3 which is out of bound
                if (x < 0 or x >= self.map.width) or (y < 0 or y >= self.map.height): continue
                self.map.data[y][x] = deepcopy(mapGame.data[y][x]) # copy information of map game to map's pacman
                # [x, y]: triple 8 tiles, then use manhattan distance to know whether food in 8 tiles x 3 or out of bound to append to tiles for eating
                new_food_scanned = [x, y] # get coordinate of 8 tiles x 3 around to know whether have food which not exists in list food_position previous
                # check if character food which we define in util.py is have in map's pacman
                if self.InitMap.food in self.map.data[y][x]:
                    # if 8 tiles x 3 have coordinate of food and this coordinate is not exists in list food_position (list foods pacman scanned and need to eat)
                    # add this coordinate to list food_position for pacman ready to eat and decrease food_count (foods pacman had seen in map)
                    if new_food_scanned not in self.food_position:
                        self.food_count -= 1
                        self.food_position.append([x, y])
                    # if foods pacman had seen in map = 0, it's mean pacman had successfully scanned all food in map
                    if self.food_count == 0: self.map_scanned = True
                # assume we have board 20x15
                # manhattan distance from node: pacman_position to goal: (4, 5)
                # if manhattan distance from node: (4, 5) to goal (food position) in 8 tiles x 3 < 3 steps, add that coordinate to list tiles
                if manhattanDistance(self.location, new_food_scanned) <= 2: tiles.append(new_food_scanned)
        return tiles

    # create some important positions for pacman go to scan around to know in pacman's area have foods, walls or monsters
    def create_important_positions(self):
        # assume that we have board 5x5
        important_position_map_scan = [] # list store important positions which pacman need to go to scan around of map
        centerLine = int(self.view / 2) # centerLine = diameter / 2 = 5 / 2 = 2
        x, y = 0, 0
        # x, y = 0 < 5, x, y = 0 + 2 = 2 -> (2, 2)
        # x = 2 < 5, y = 0 < 5, x = 2 + 2 = 4, y = 0 + 2 = 2 -> (4, 2)
        while x < self.map.width:
            x = x + centerLine
            # x = 0 < 5, y = 2 < 5, x = 0 + 2 = 2, y = 2 + 2 = 4 -> (2, 4)
            # x = 2 < 5, y = 2 < 5, x = 2 + 2 = 4, y = 2 + 2 = 4 -> (4, 4)
            y = 0
            while y < self.map.height:
                y = y + centerLine
                # avoid position is out of bound
                if x >= self.map.width or y >= self.map.height: break
                important_position_map_scan.append([x, y]) # add that important position to list
        return important_position_map_scan # return list important positions for pacman move to

    # check if important positions collision with wall, remove it from list to make pacman avoid going that positions
    # if pacman have reach to these important positions, remove its position
    def check_important_positions_collision_walls(self):
        # if pacman scanned and have full view of map, pacman won't need check important positions collision with walls
        if self.godEye == True: return
        for goal in self.goal_state:
            # (2, 2), (2, 4)...(2, 18), (4, 2),...(4,18), (6, 2),...(6, 18)...
            x_coordinate, y_coordinate = goal[0], goal[1] # get coordinate of important position to check if it collisions with walls
            if self.InitMap.wall in self.map.data[y_coordinate][x_coordinate]:
                self.goal_state.remove(goal) # if important position pacman will go to collision with wall, remove it from list important positions

    # find best move to closest food from successor
    def food_best_move(self):
        # if pacman scanned and have full view of map or level of pacman is 1 or 2
        if self.godEye == True: nearestCapsule, foodDist = self.closest_capsule(self.food_position) # get food position with min distance for pacman eating
        else:
            # if pacman didn't scan full view of map and still have food which pacman didn't scanned
            if self.map_scanned == False or self.food_count > 0:
                self.check_important_positions_collision_walls() # check important positions pacman will go collision with walls
                self.remove_duplicate_important_positions() # remove important positions which pacman had gone to avoid a important position pacman scan twice
                nearestFood, foodDist = self.closest_capsule(self.goal_state) # get food position with min distance if pacman scanned and finded nearest food from important positions
            # if pacman scanned all food around and not exist food any more for pacman to find
            # empty food_count if pacman went to important positions
            elif self.food_count <= 0: nearestFood = []
            nearest_food, foodDist = self.closest_capsule(self.food_position) # get food position with min distance
            # if empty, copy nearest food from nearest food position previous
            if len(nearest_food) == 0: nearestCapsule = deepcopy(nearestFood) # if nearest_food fully eat, back to nearestFood(important positions) to continue scan for nearest food
            else: nearestCapsule = deepcopy(nearest_food)
        bestMove = [] # list store best move for pacman eating food
        # if pacman stand right of nearest food, go left
        if self.location[0] > nearestCapsule[0]: bestMove.append("left")
        # if pacman stand left of nearest food, go right
        if self.location[0] < nearestCapsule[0]: bestMove.append("right")
        # if pacman stand down of nearest food, go up
        if self.location[1] > nearestCapsule[1]: bestMove.append("up")
        # if pacman stand up of nearest food, go down
        if self.location[1] < nearestCapsule[1]: bestMove.append("down")
        return bestMove # return list best moves for eating food with min distance

    # eat food when pacman scanned position of foods
    def eat_food(self):
        self.food -= 1
        # if empty food, pacman win the game
        if self.food <= 0: return util.isWin()
        return None

    # evaluation which food is closest for pacman to eat in 8 tiles x 3
    def closest_capsule(self, caps_pos):
        '''
        # this evaluation function should be improved for better scanning food
        min_food_distance = -1
        nearestFood = []
        for foods in betterFood:
            newFood_x, newFood_y = foods[0], foods[1]
            dist = manhattanDistance([x_pacman, y_pacman], [newFood_x, newFood_y])
            if min_food_distance >= dist or min_food_distance == -1:
                min_food_distance = dist
                nearestFood = deepcopy(foods)
        return nearestFood, min_food_distance
        '''
        INFINITY = 99999
        x_pacman, y_pacman = self.location[0], self.location[1] # get pacman position
        foodDist = INFINITY
        nearestCapsule = [] # list store for nearest food for pacman eating
        for caps in caps_pos:
            newFood_x, newFood_y = caps[0], caps[1] # get food nearests
            dist = manhattanDistance([x_pacman, y_pacman], [newFood_x, newFood_y]) # compute distance from pacman position to position of foods nearests
            # get min distance (food with min distance to pacman position)
            if dist < foodDist:
                foodDist = dist
                nearestCapsule = deepcopy(caps) # copy positions for list nearest for pacman know which food is nearest
        return nearestCapsule, foodDist

    # random move pacman instead of stopping at a fixed position
    def random_move(self, move):
        # if pacman have another possible move beside stop action, make pacman move instead of stopping at a fixed position
        if len(move) > 1:
            try: move.remove("stop")
            except ValueError: pass
        for direction in move:
            x_pacman, y_pacman = self.location[0], self.location[1] # get position of pacman
            new_location_pacman = [] # list store new position when pacman moving
            if direction == "left": new_location_pacman = [x_pacman - 1, y_pacman] # add new position pacman after moving left to list
            elif direction == "right": new_location_pacman = [x_pacman + 1, y_pacman] # add new position pacman after moving right to list
            elif direction == "up": new_location_pacman = [x_pacman, y_pacman - 1] # add new position pacman after moving up to list
            elif direction == "down": new_location_pacman = [x_pacman, y_pacman + 1] # add new position pacman after moving down to list
            # if new_location random is come back to previous location but pacman have another direction which pacman can go
            # remove that direction to make pacman go another direction to help pacman scan full view of map
            if self.previous_location == new_location_pacman:
                if len(move) > 1: move.remove(direction) # remove direction which make pacman can go back previous position if pacman have another direction to move
                # if not exist another direction pacman can move
                elif len(move) == 1:
                    for action in self.actions:
                        if action == "stop" or action == direction: continue # pacman can stop or move only that direction
                        move.append(action)
                    # check if can remove current direction
                    if len(move) == 1: break # only direction pacman can go, but it can make pacman go back previous position, pacman should stop and avoid as much as possible duplicate path went through
                    move.remove(direction) # remove current direction which make pacman go back previous position
        return move[randint(0, len(move) - 1)] # random valid actions which pacman can move

    # avoid pacman go to important positions twice
    def remove_duplicate_important_positions(self):
        for goal in self.goal_state:
            x_pos, y_pos = goal[0], goal[1]
            # default: 0 (not visited), if visited remove it to avoid going an important position twice
            if self.map.visitedMap[y_pos][x_pos] == 1:
                self.goal_state.remove(goal)

    # scan positions around important positions, if these postion have food, eating, then remove these positions from goal position
    # because we want pacman can go to all important positions as much as possible to scan and know more information about map
    def scan_positions_around_important_positions(self):
        x_pacman, y_pacman = self.location[0], self.location[1] # get pacman current position
        self.map.visitedMap[y_pacman][x_pacman] = 1 # mark current position pacman is standing as visited
        # if pacman didn't scan full view of map
        if self.map_scanned == False:
            # remove positions pacman scanned but that positions is not important positions
            try: self.goal_state.remove([x_pacman, y_pacman])
            except ValueError: pass
        # remove position of food from list food_position (list which pacman use to detect food while scanning)
        try: self.food_position.remove([x_pacman, y_pacman])
        except ValueError: pass
        # remove that food from map after pacman eating
        try: self.map.destroyFood([x_pacman, y_pacman])
        except: pass

    # if level is 1, 2 or pacman scanned all map, pacman will get full view of map for food positions
    def fullViewOfMap(self, mapGame):
        self.godEye, self.map_scanned, self.map = True, True, mapGame
        for x in range(self.map.width):
            for y in range(self.map.height):
                # if the map exists food
                if self.InitMap.food in self.map.data[y][x]:
                    self.food_position.append([x, y]) # add position all foods of map to list food_position for pacman find to eat