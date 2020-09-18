# set all row and column as not visited
# {(0, 0): 0...(24,24): 0}
# 0: not visited, 1: visited
def set_not_visitied(adjacent_matrix):
    dictionary = {}
    for x in range(len(adjacent_matrix)):
        for y in range(len(adjacent_matrix[x])): dictionary[(x, y)] = 0
    return dictionary

def path_visited(adjacent_matrix):
    dictionary = {}
    for x in range(len(adjacent_matrix)):
        for y in range(len(adjacent_matrix[x])): dictionary[(x, y)] = (-1, -1)  # path = [False] * -1, make all vertices as not visited
    return dictionary

# return manhattan distance between two points start and end
def manhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_ele_stack(stack):
    if len(stack) == 0: return None
    temp = []
    cost_min = 10000000000
    for i in range(len(stack)):
        if stack[i][1] == cost_min:
            temp.append(stack[i])
        elif stack[i][1] < cost_min:
            temp.clear()
            cost_min = stack[i][1]
            temp.append(stack[i])
    min_path = temp[0][0]
    stack.remove((min_path, cost_min))
    return min_path, cost_min

def check_stack(new_ele, stack):
    for i in range(len(stack)):
        path, cost = stack[i]
        if new_ele == path: return True, cost, i
    return False, None, None

def Astar_Level1(adjacent_matrix, visitied, path, x_pacman, y_pacman, x_food, y_food):
    stack = []
    stack.append(((x_pacman, y_pacman), manhattanDistance(x_pacman, y_pacman, x_food, y_food)))
    while stack:
        s, cost = get_ele_stack(stack)  # take s and cost_of_s
        cost = cost - manhattanDistance(s[0], s[1], x_food, y_food)
        visitied[(s[0], s[1])] = 1  # store for each node visited
        if s == (x_food, y_food): return backtrack(path, x_pacman, y_pacman, x_food, y_food)
        # go down == 0
        if visitied[(s[0] + 1, s[1])] == 0 and adjacent_matrix[s[0] + 1][s[1]] != 1:
            cost_new = cost + 1 + manhattanDistance(s[0] + 1, s[1], x_food, y_food)
            new_ele = ((s[0] + 1, s[1]), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0] + 1, s[1])] == 0:
                stack.append(new_ele)
                path[(s[0] + 1, s[1])] = s  # record its parent
            elif in_stack == True and visitied[(s[0] + 1, s[1])] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0] + 1, s[1]))
                path[(s[0] + 1, s[1])] = s
        # go top == 0
        if visitied[(s[0] - 1, s[1])] == 0 and adjacent_matrix[s[0] - 1][s[1]] != 1:
            cost_new = cost + 1 + manhattanDistance(s[0] - 1, s[1], x_food, y_food)
            new_ele = ((s[0] - 1, s[1]), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0] - 1, s[1])] == 0:
                stack.append(new_ele)
                path[(s[0] - 1, s[1])] = s  # record its parent
            elif in_stack == True and visitied[(s[0] - 1, s[1])] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0] - 1, s[1]))
                path[(s[0] - 1, s[1])] = s
        # go right == 0
        if visitied[(s[0], s[1] + 1)] == 0 and adjacent_matrix[s[0]][s[1] + 1] != 1:
            cost_new = cost + 1 + manhattanDistance(s[0], s[1] + 1, x_food, y_food)
            new_ele = ((s[0], s[1] + 1), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0], s[1] + 1)] == 0:
                stack.append(new_ele)
                path[(s[0], s[1] + 1)] = s  # record its parent
            elif in_stack == True and visitied[(s[0], s[1] + 1)] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0], s[1] + 1))
                path[(s[0], s[1] + 1)] = s
        # go left == 0
        if visitied[(s[0], s[1] - 1)] == 0 and adjacent_matrix[s[0]][s[1] - 1] != 1:
            cost_new = cost + 1 + manhattanDistance(s[0], s[1] - 1, x_food, y_food)
            new_ele = ((s[0], s[1] - 1), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0], s[1] - 1)] == 0:
                stack.append(new_ele)
                path[(s[0], s[1] - 1)] = s  # record its parent
            elif in_stack == True and visitied[(s[0], s[1] - 1)] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0], s[1] - 1))
                path[(s[0], s[1] - 1)] = s
    return "No path for pacman moving"

def Astar_Level2(adjacent_matrix, visitied, path, x_pacman, y_pacman, x_food, y_food):
    stack = []
    stack.append(((x_pacman, y_pacman), manhattanDistance(x_pacman, y_pacman, x_food, y_food)))
    while stack:
        s, cost = get_ele_stack(stack)  # take s and cost_of_s
        cost = cost - manhattanDistance(s[0], s[1], x_food, y_food)
        visitied[(s[0], s[1])] = 1  # store for each node visited
        if s == (x_food, y_food): return backtrack(path, x_pacman, y_pacman, x_food, y_food)
        # go down == 0
        if visitied[(s[0] + 1, s[1])] == 0 and adjacent_matrix[s[0] + 1][s[1]] != 1 and adjacent_matrix[s[0] + 1][
            s[1]] != 3:
            cost_new = cost + 1 + manhattanDistance(s[0] + 1, s[1], x_food, y_food)
            new_ele = ((s[0] + 1, s[1]), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0] + 1, s[1])] == 0:
                stack.append(new_ele)
                path[(s[0] + 1, s[1])] = s  # record its parent
            elif in_stack == True and visitied[(s[0] + 1, s[1])] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0] + 1, s[1]))
                path[(s[0] + 1, s[1])] = s
        # go top == 0
        if visitied[(s[0] - 1, s[1])] == 0 and adjacent_matrix[s[0] - 1][s[1]] != 1 and adjacent_matrix[s[0] - 1][
            s[1]] != 3:
            cost_new = cost + 1 + manhattanDistance(s[0] - 1, s[1], x_food, y_food)
            new_ele = ((s[0] - 1, s[1]), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0] - 1, s[1])] == 0:
                stack.append(new_ele)
                path[(s[0] - 1, s[1])] = s  # record its parent
            elif in_stack == True and visitied[(s[0] - 1, s[1])] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0] - 1, s[1]))
                path[(s[0] - 1, s[1])] = s
        # go right == 0
        if visitied[(s[0], s[1] + 1)] == 0 and adjacent_matrix[s[0]][s[1] + 1] != 1 and adjacent_matrix[s[0]][
            s[1] + 1] != 3:
            cost_new = cost + 1 + manhattanDistance(s[0], s[1] + 1, x_food, y_food)
            new_ele = ((s[0], s[1] + 1), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0], s[1] + 1)] == 0:
                stack.append(new_ele)
                path[(s[0], s[1] + 1)] = s  # record its parent
            elif in_stack == True and visitied[(s[0], s[1] + 1)] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0], s[1] + 1))
                path[(s[0], s[1] + 1)] = s
        # go left == 0
        if visitied[(s[0], s[1] - 1)] == 0 and adjacent_matrix[s[0]][s[1] - 1] != 1 and adjacent_matrix[s[0]][
            s[1] - 1] != 3:
            cost_new = cost + 1 + manhattanDistance(s[0], s[1] - 1, x_food, y_food)
            new_ele = ((s[0], s[1] - 1), cost_new)
            in_stack, cost_old, pos = check_stack(new_ele, stack)
            if in_stack == False and visitied[(s[0], s[1] - 1)] == 0:
                stack.append(new_ele)
                path[(s[0], s[1] - 1)] = s  # record its parent
            elif in_stack == True and visitied[(s[0], s[1] - 1)] == 0 and cost_old > cost_new:
                stack.pop(pos)
                stack.append(new_ele)
                path.pop((s[0], s[1] - 1))
                path[(s[0], s[1] - 1)] = s
    return "No path for pacman moving"

# backtrack for path returns of each node correspond to its parent
def backtrack(path, x_pacman, y_pacman, x_food, y_food):
    result = []
    # if vertices food not visited
    if path[(x_food, y_food)] == (-1, -1): return result
    result.append((x_food, y_food))  # append that position food to list result
    # if food position != pacman position
    while path[(x_food, y_food)] != (x_pacman, y_pacman):
        result.append(path[(x_food, y_food)])
        (x_food, y_food) = path[(x_food, y_food)]
    result.append((x_pacman, y_pacman))
    result.reverse()  # backtrack from down to top, so we have to reverse result to get path returns
    return result