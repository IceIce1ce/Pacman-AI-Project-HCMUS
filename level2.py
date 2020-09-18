import turtle
import math
import searchLevel1_2 as sea
import time

def SplitCharacter(line):
    return [int(charac) for charac in line] # split each character of line and convert to int

def readFile(myFile):
    f = open(myFile, 'r')
    myfile_data = f.readline()
    x = myfile_data.split() # read size of map
    blank_space = x[-1].split('x')
    row = int(blank_space[0]) # row of map
    col = int(blank_space[1]) # column of map
    matrix = f.readlines()  # read matrix until EOF
    adjacent_matrix = [] # list store matrix
    for line in matrix:
        y = line.split()
        z = SplitCharacter(y[-1])
        adjacent_matrix.append(z) # append matrix to list
    f.close()
    return row, col, adjacent_matrix

row, col, adjacent_matrix = readFile("map_2.txt")

# top left block: (-288, 288), top right block: (288, 288), bottom left block: (-288, -288), bottom right block: (288, -288)
# 0, 24, 24, 48, 48,...288
# column, row even: width or height / 2, else (width or height - 24) / 2
# width = row * pixel_per_cell
# height = col * pixel_per_cell
pixel_per_cell = 24 # each cell has pixel = 24

# setup background game
wn = turtle.Screen()
wn.bgpic("image/theme.gif")
wn.title("Pacman AI")
wn.setup(1600, 900)

# register shapes (use only with .gif image)
turtle.register_shape("image/wall_img1.gif")
turtle.register_shape("image/food.gif")
turtle.register_shape("image/pacman_top.gif")
turtle.register_shape("image/pacman_bottom.gif")
turtle.register_shape("image/pacman_left.gif")
turtle.register_shape("image/pacman_right.gif")
turtle.register_shape("image/monster.gif")

class Map(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("image/wall_img1.gif")
        self.penup()
        self.speed(0)

class Food(turtle.Turtle):
    def __init__(self, x_food, y_food):
        turtle.Turtle.__init__(self)
        self.shape("image/food.gif")
        self.penup()
        self.speed(0)
        self.reward = 20
        self.goto(x_food, y_food)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Monster(turtle.Turtle):
    def __init__(self, x_monster, y_monster):
        turtle.Turtle.__init__(self)
        self.shape("image/monster.gif")
        self.penup()
        self.speed(0)
        self.goto(x_monster, y_monster)

class Pacman(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("image/pacman_right.gif")
        self.penup()
        self.speed(1)
        self.point = 0

    def go_up(self):
        move_to_x = pacman.xcor()
        move_to_y = pacman.ycor() + pixel_per_cell
        self.shape("image/pacman_top.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = pacman.xcor()
        move_to_y = pacman.ycor() - pixel_per_cell
        self.shape("image/pacman_bottom.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = pacman.xcor() - pixel_per_cell
        move_to_y = pacman.ycor()
        self.shape("image/pacman_left.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = pacman.xcor() + pixel_per_cell
        move_to_y = pacman.ycor()
        self.shape("image/pacman_right.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2)) # euclidean distance
        if distance < 5:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

walls = []
foods = []
monsters = []

def setup_maze(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            character = level[x][y] # get character at coordinate x, y
            # calc screen x, y coordinate
            screen_x = -288 + (y * pixel_per_cell) # -288 + (y * 24)
            screen_y = 288 - (x * pixel_per_cell) # 288 - (x * 24)
            # check if it is wall
            if character == 1:
                map.goto(screen_x, screen_y)
                map.stamp()
                walls.append((screen_x, screen_y)) # add coordinate to wall list
            # check if it is pacman
            if character == 4:
                pacman.goto(screen_x, screen_y)
                x_pacman = x
                y_pacman = y
            # check if it is food
            if character == 2:
                foods.append(Food(screen_x, screen_y))
                x_food = x
                y_food = y
            # check if it is monster
            if character == 3:
                monsters.append(Monster(screen_x, screen_y))
                x_monster = x
                y_monster = y

map = Map()
pacman = Pacman()

x_pacman, y_pacman, x_food, y_food, x_monster, y_monster = 0, 0, 0, 0, 0, 0

for x in range(len(adjacent_matrix)):
    for y in range(len(adjacent_matrix[x])):
        character = adjacent_matrix[x][y]
        if character == 4:
            x_pacman = x
            y_pacman = y
        if character == 2:
            x_food = x
            y_food = y
        if character == 3:
            x_monster = x
            y_monster = y

setup_maze(adjacent_matrix)
visited = sea.set_not_visitied(adjacent_matrix)
pathVisited = sea.path_visited(adjacent_matrix)
sea.Astar_Level2(adjacent_matrix, visited, pathVisited, x_pacman, y_pacman, x_food, y_food)
BackTrack = sea.backtrack(pathVisited, x_pacman, y_pacman, x_food, y_food)
print("The length of the discovered paths:", len(BackTrack))
f1 = open("path_discorved/output_level2.txt", "a")
f1.write("Path discovered of level 2: ")
f1.write(str(BackTrack))
f1.write('\n')
f1.write("The length of the discovered paths in level 2: ")
f1.write(str(len(BackTrack)))
f1.write('\n')
f1.close()

def getCoordinate(path):
    result = []
    for i in range(len(path)):
        getBackTrack = path[i]
        Dx = -288 + getBackTrack[1] * pixel_per_cell  # -288 + y * 24
        Dy = 288 - getBackTrack[0] * pixel_per_cell  # 288 - x * 24
        result.append((Dx, Dy))
    if not result: print("No path for pacman moving")
    return result

getNextCell = getCoordinate(BackTrack)

# check for pacman collision with food
def eat():
    for food in foods:
        if pacman.is_collision(food):
            pacman.point += food.reward # add point to pacman after eating a food
            print("Point of pacman: ", pacman.point)
            f2 = open("path_discorved/output_level2.txt", "a")
            f2.write("Point of pacman in level 2: ")
            f2.write(str(pacman.point))
            f2.write('\n')
            f2.close()
            food.destroy() # destroy the food after eating
            foods.remove(food) # remove that from from foods list

def mainLevel2():
    time_start_event = time.time()
    while True:
        if len(getNextCell) > 0:
            for i in range(len(getNextCell)):
                currentPositionPacman = (pacman.xcor(), pacman.ycor())
                cell = getNextCell[i]
                Dx, Dy = cell[0] - currentPositionPacman[0], cell[1] - currentPositionPacman[1]
                # decrease -1 point when pacman is moving up
                if Dx == 0 and Dy == pixel_per_cell:
                    pacman.go_up()
                    pacman.point -= 1
                    eat()
                # decrease -1 point when pacman is moving down
                elif Dx == 0 and Dy == -pixel_per_cell:
                    pacman.go_down()
                    pacman.point -= 1
                    eat()
                # decrease -1 point when pacman is moving right
                elif Dx == pixel_per_cell and Dy == 0:
                    pacman.go_right()
                    pacman.point -= 1
                    eat()
                # decrease -1 point when pacman is moving left
                elif Dx == -pixel_per_cell and Dy == 0:
                    pacman.go_left()
                    pacman.point -= 1
                    eat()
        time_end_event = time.time()
        total_time_finished = time_end_event - time_start_event
        delta = str(round(total_time_finished, 2))
        print("Time to finished:", delta + "s")
        f3 = open("path_discorved/output_level2.txt", "a")
        f3.write("Time to finish in level 2: ")
        f3.write(str(delta))
        f3.write("s")
        f3.close()
        wn.tracer(0)
        wn.update()
        wn.bye()