from util import *
from setting import *
import pygame
from copy import deepcopy

class Map:
    # init for map
    def __init__(self, width, height):
        self.width = width # width of map
        self.height = height # height of map
        self.InitMap = initGame()
        loading_map = [] # create an empty list for loading map
        self.data = [[loading_map for y in range(height)] for x in range(width)] # coordinate x define for width of map, coordinate y define for height of map, store data height and width for each map
        self.visitedMap = [[0 for y in range(height)] for x in range(width)] # set all cell in map as not visited (0), if pacman visited, mark that cell as visited (1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # screen of pygame
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS

    # update new location for agent (pacman, monster) in map after each step moving
    def update(self, current_location, new_location, characterMap):
        # current_location: current position of agents (pacman, monsters)
        # new_location: new position of agents (pacman, monsters) after moving
        # characterMap: 3: monster, 4: pacman
        x_pos, y_pos = current_location[0], current_location[1] # coordinate for agent's current location
        new_x_pos, new_y_pos = new_location[0], new_location[1] # coordinate for agent's new location
        try:
            self.data[y_pos][x_pos].remove(characterMap) # remove agent from current location
            # if initial state (current location) == None
            if len(self.data[y_pos][x_pos]) == 0: self.data[y_pos][x_pos] = deepcopy([]) # return empty position if initial state is empty
        except ValueError: pass
        # update agent new location
        newState = deepcopy(self.data[new_y_pos][new_x_pos]) # take coordinate of new position
        newState.append(characterMap) # add characterMap to new location after removing that characterMap from old location
        self.data[new_y_pos][new_x_pos] = deepcopy(newState) # update info of new location

    # helper function
    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def copy(self):
        g = Map(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def shallowCopy(self):
        g = Map(self.width, self.height)
        g.data = self.data
        return g

    def deepCopy(self):
        return self.copy()

    def __eq__(self, other):
        # allows two states to be compared
        if other == None: return False
        return self.data == other.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # allows states to be keys of dictionaries
        return hash(self.data)

    def __str__(self):
        return str(self.data)
    # helper function

    # draw map
    def start_draw(self):
        # draw background
        background = pygame.image.load("image/theme.gif") # load image
        self.screen.blit(background, (0, 0)) # draw in buffer
        for y in range(self.height):
            for x in range(self.width):
                # if character pacman in initmap = 4 same to mapData, draw pacman
                if self.InitMap.pacman in self.data[y][x]:
                    # pygame.draw.circle(self.screen, PLAYER_COLOR, (int(x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2, int(y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), int(self.cell_width // 5.5))
                    pacmanImg = pygame.image.load("image/pacman_right.gif")
                    self.screen.blit(pacmanImg, (int(x * self.cell_width) + self.cell_width // 2.5 + TOP_BOTTOM_BUFFER // 2.5, int(y * self.cell_height) + self.cell_height // 3 + TOP_BOTTOM_BUFFER // 3))
                # if character wall in initmap = 1 same to mapData, draw wall
                elif self.InitMap.wall in self.data[y][x]:
                    # draw grid
                    # pygame.draw.line(self.screen, (52, 82, 235), (x * self.cell_width + TOP_BOTTOM_BUFFER // 2, 0), (x * self.cell_width + TOP_BOTTOM_BUFFER // 2, HEIGHT))
                    # pygame.draw.line(self.screen, (52, 82, 235), (0, x * self.cell_height + TOP_BOTTOM_BUFFER // 2), (WIDTH, x * self.cell_height + TOP_BOTTOM_BUFFER // 2))
                    # draw wall
                    pygame.draw.rect(self.screen, (52, 82, 235), (x * self.cell_width + TOP_BOTTOM_BUFFER // 2, y * self.cell_height + TOP_BOTTOM_BUFFER // 2, self.cell_width, self.cell_height))
                # if character food in initmap = 2 same to mapData, draw food
                elif self.InitMap.food in self.data[y][x]:
                    pygame.draw.circle(self.screen, WHITE, (int(x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2, int(y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)
                # if character monster in initmap = 3 same to mapData, draw monster
                elif self.InitMap.monster in self.data[y][x]:
                    # pygame.draw.circle(self.screen, GREEN, (int(x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2, int(y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), int(self.cell_width // 5.5))
                    monsterImg = pygame.image.load("image/monster.gif")
                    self.screen.blit(monsterImg, (int(x * self.cell_width) + self.cell_width // 2.5 + TOP_BOTTOM_BUFFER // 2.5, int(y * self.cell_height) + self.cell_height // 3 + TOP_BOTTOM_BUFFER // 3))
        pygame.display.update()
        # pygame.time.delay(200) # change this value for suitable speed of game

    # get resolution of map for pacman because we want pacman to learn and get full view map during scanning
    def getResolutionMap(self):
        return [self.width, self.height]

    # add fixed index of foods into map
    def getFood(self, foods):
        for idx in foods: self.update(idx, idx, self.InitMap.food)

    # add fixed index of walls into map
    def getWall(self, walls):
        for idx in walls: self.update(idx, idx, self.InitMap.wall)

    # add agents(pacman, monsters) into map
    def getAgent(self, agents):
        for agent in agents: self.update(agent.location, agent.location, agent.myInitMap) # self.myInitMap.pacman or self.myInitMap.monster

    # remove food at index which pacman ate from map
    def destroyFood(self, food_index):
        x_food, y_food = food_index[0], food_index[1] # get fixed index of food
        try: self.data[y_food][x_food].remove(self.InitMap.food) # remove from map after pacman eating
        except ValueError: pass