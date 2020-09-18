from pacman import *
from ghostAgents import *
from setup_map import *
from util import *
from setting import *
import time

# init pygame and character of map
pygame.init()
pygame.display.set_caption("Pacman AI")
initCharacter = initGame()

# check final state result of pacman is win or lose
def printResult(pacman):
    result = pacman.eat_food()
    if result == "win": return "Pacman win the game"
    else: return "Pacman lose the game"

# get valid actions of agents(pacman, monsters) and avoid agents go out of bound
def valid_actions(agent, mapGame, level):
    # agent: pacman, monster
    # mapGame: map of pacman world
    # game_level: 4 levels
    x_agent, y_agent = agent.location[0], agent.location[1] # get current position of agent (pacman, monster)
    agent.actions = ["up", "left", "down", "right", "stop"] # init actions of agents
    # check position of agents from left of map to right
    if x_agent > 0:
        # if left direction of agent has wall, remove direction left
        if initCharacter.wall in mapGame.data[y_agent][x_agent - 1]: agent.getDistribution("left")
        # if level is 1 or 2, assume monster as wall and remove direction which monster appear left direction
        if level < 3:
            if initCharacter.monster in mapGame.data[y_agent][x_agent - 1]: agent.getDistribution("left")
    # else remove direction left if x_agent <= 0 to avoid agent go out of bound
    elif x_agent <= 0: agent.getDistribution("left")
    # check position of agents from right of map to left
    if x_agent < mapGame.width - 1:
        # if right direction of agent has wall, remove direction right
        if initCharacter.wall in mapGame.data[y_agent][x_agent + 1]: agent.getDistribution("right")
        # if level is 1 or 2, assume monster as wall and remove direction which monster appear in right direction
        if level < 3:
            if initCharacter.monster in mapGame.data[y_agent][x_agent + 1]: agent.getDistribution("right")
    # else remove direction right if x_agent >= mapGame.width - 1 to avoid agent go out of bound
    elif x_agent >= mapGame.width - 1: agent.getDistribution("right")
    # check position of agents from up of map to down
    if y_agent > 0:
        # if up direction of agent has wall, remove direction up
        if initCharacter.wall in mapGame.data[y_agent - 1][x_agent]: agent.getDistribution("up")
        # if level is 1 or 2, assume monster as wall and remove direction which monster appear in up direction
        if level < 3:
            if initCharacter.monster in mapGame.data[y_agent - 1][x_agent]: agent.getDistribution("up")
    # else remove direction up if y_agent <= 0 to avoid agent go out of bound
    elif y_agent <= 0: agent.getDistribution("up")
    # check position of agents from down of map to up
    if y_agent < mapGame.height - 1:
        # if down direction of agent has wall, remove direction down
        if initCharacter.wall in mapGame.data[y_agent + 1][x_agent]: agent.getDistribution("down")
        # if level is 1 or 2, assume monster as wall and remove direction which monster appear in down direction
        if level < 3:
            if initCharacter.monster in mapGame.data[y_agent + 1][x_agent]: agent.getDistribution("down")
    # else remove direction down if y_agent >= mapGame.height - 1 to avoid agent go out of bound
    elif y_agent >= mapGame.height - 1: agent.getDistribution("down")

# draw text graphic
def draw_text(words, screen, position, size, color, fontName):
    font = pygame.font.SysFont(fontName, size)
    text = font.render(words, False, color)
    screen.blit(text, position)
    pygame.display.update()
    pygame.time.delay(500)

# check current state is win or lose
def check_current_state(pacman, mapGamme, screen):
    x_pacman, y_pacman = pacman.location[0], pacman.location[1] # get current position of pacman
    # if food is in current position of pacman
    if initCharacter.food in mapGamme.data[y_pacman][x_pacman]:
        result = pacman.eat_food()
        mapGamme.destroyFood([x_pacman, y_pacman]) # remove food from list food
        if result == "win": return "WIN" # if state == 'win'
    # if current position of pacman is collision with monster
    if initCharacter.monster in mapGamme.data[y_pacman][x_pacman]: return "DIE"
    return False

def mainLevel3_4():
    mapSize = []  # list store size of map
    level = int(input("Input your level (3-4): ")) # level 3 and 4 of game
    while level <= 2 or level >= 5:
        print("Level of game isn't exist, try-again !!!")
        level = int(input("Input your level (3-4): "))
    wall = input("Input type of wall (3-5): ") # 5 maps of game
    while wall <= '2' or wall >= '6':
        print("File of map isn't exist, try-again !!! ")
        wall = input("Input type of wall (3-5): ")
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # get default resolution of pygame
    type_of_map = "map_" + wall + ".txt" # read 5 files of map game
    agentRule, wallPosition, foodPosition, pacmanPosition, monsterPosition = [], [], [], None, [] # add walls, foods, pacman and monsters to map
    # read map from file
    with open(type_of_map, 'r', ) as file:
        for yidx, line in enumerate(file):
            if yidx == 0:
                for index in range(0, len(line) - 1):
                    if line[index] == "x":
                        mapSize.append(int(line[:index]))
                        mapSize.append(int(line[index + 1:]))
            else:
                for xidx, char in enumerate(line):
                    # if character is 1, add walls to map
                    if char == "1": wallPosition.append([xidx, yidx - 1])
                    # if character is 2, add foods to map
                    elif char == "2": foodPosition.append([xidx, yidx - 1])
                    # if character is 4, add pacman to map
                    elif char == "4": pacmanPosition = [xidx, yidx - 1]
                    # if level is 2, 3, 4 and character is 3, add monster to map
                    if level != 1:
                        if char == "3": monsterPosition.append([xidx, yidx - 1])
    # if default map game is 5x5, 10x10, 15x15... -> ignore
    # if default map game such as 10x8, make it become 10x10 so we'll get full important positions for map 10x10 without ignoring any tiles
    mapGame = Map(mapSize[0], mapSize[1] + abs(mapSize[0] - mapSize[1]))
    food_position = foodPosition # get position of food in map
    total_food = len(food_position) # get total food map provided
    wall_pos = wallPosition # get position of wall in map
    map_resolution = mapGame.getResolutionMap() # get resolution of map
    pacman = PacmanRules(pacmanPosition, 5, map_resolution, total_food, level) # 5 is fixed number of diameter when calculate 8 tiles x 3 for pacman
    agentRule.append(pacman) # add pacman to list agentRule
    for enemies in monsterPosition:
        monster = GhostRules(enemies, 5, map_resolution, level) # 5 is fixed number of diameter when calculate 8 tiles x 3 for monsters
        agentRule.append(monster) # add monster to list agentRule
    mapGame.getAgent(agentRule) # add agent (pacman, monsters) into the map
    mapGame.getFood(food_position) # add foods into the map
    mapGame.getWall(wall_pos) # add walls into the map
    mapGame.start_draw() # draw map game
    check_current_state(pacman, mapGame, screen) # start current event
    i = 100000 # count total steps pacman finish the game to compute point of pacman
    time_start_event = time.time()
    while True:
        for a in agentRule:
            valid_actions(a, mapGame, level) # get valid actions of agents (pacman, monster)
            a.move(mapGame) # after each step moving, update agents (pacman, monsters) new position
        finishEvent = check_current_state(pacman, mapGame, screen) # finish current event
        mapGame.start_draw()
        if finishEvent == "WIN":
            draw_text('Pacman win', screen, [WIDTH // 2.6, 320], 52, YELLOW, FONT)
            print("Pacman win the game")
            print("The length of the discovered paths:", 100000 - i)
            pacmanPointWin = (total_food - pacman.food) * 20
            totalMovingStepsWin = 100000 - i
            totalPointPacmanWin = -totalMovingStepsWin + pacmanPointWin
            print("Point of pacman:", totalPointPacmanWin)
            break
        elif finishEvent == "DIE":
            draw_text('Pacman die', screen, [WIDTH // 2.6, 320], 52, YELLOW, FONT)
            print("Pacman lose the game")
            print("The length of the discovered paths:", 100000 - i)
            pacmanPointLose = (total_food - pacman.food) * 20
            totalMovingStepsLose = 100000 - i
            totalPointPacmanLose = -totalMovingStepsLose + pacmanPointLose
            print("Point of pacman:", totalPointPacmanLose)
            break
        i = i - 1 # decrease i after each step moving of pacman
        if i <= 0: break
        # discovered path of pacman
        x_discovered, y_discovered = pacman.location[0], pacman.location[1]
        path_discovered = [x_discovered, y_discovered]
        f1 = open("path_discorved/output_level3.txt", "a")
        f2 = open("path_discorved/output_level4.txt", "a")
        total_length_discovered = 100000 - i
        if level == 3:
            f1.write("Path discovered of level 3: ")
            f1.write(str(path_discovered))
            f1.write('\n')
            f1.write("The length of the discovered paths in level 3: ")
            f1.write(str(total_length_discovered))
            f1.write('\n')
            f1.close()
        elif level == 4:
            f2.write("Path discovered of level 4: ")
            f2.write(str(path_discovered))
            f2.write('\n')
            f2.write("The length of the discovered paths in level 4: ")
            f2.write(str(total_length_discovered))
            f2.write('\n')
            f2.close()
    time_end_event = time.time()
    total_time_finished = time_end_event - time_start_event
    delta = str(round(total_time_finished, 2))
    print("Time to finished:", delta + "s")
    pacmanPoint = (total_food - pacman.food) * 20
    totalMovingSteps = 100000 - i
    totalPointPacman = -totalMovingSteps + pacmanPoint
    finalResult = printResult(pacman)
    if level == 3:
        f3 = open("path_discorved/output_level3.txt", "a")
        f3.write(finalResult)
        f3.write('\n')
        f3.write("Point of pacman in level 3: ")
        f3.write(str(totalPointPacman))
        f3.write('\n')
        f3.write("Time to finish in level 3: ")
        f3.write(str(delta))
        f3.write("s")
        f3.close()
    elif level == 4:
        f4 = open("path_discorved/output_level4.txt", "a")
        f4.write(finalResult)
        f4.write('\n')
        f4.write("Point of pacman in level 4: ")
        f4.write(str(totalPointPacman))
        f4.write('\n')
        f4.write("Time to finish in level 4: ")
        f4.write(str(delta))
        f4.write("s")
        f4.close()
    pygame.quit()