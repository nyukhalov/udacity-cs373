# -------------------
# Background Information
#
# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
# 
# For example:
#
# warehouse = [[ 1, 2, 3],
#              [ 0, 0, 0],
#              [ 0, 0, 0]]
# dropzone = [2,0] 
# todo = [2, 1]
# 
# The robot starts at the dropzone.
# The dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to the dropzone.
#
# Robot can move diagonally, but the cost of a diagonal move is 1.5.
# The cost of moving one step horizontally or vertically is 1.
# So if the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, the robot has to move into the same cell as the box.
# When the robot picks up a box, that cell becomes passable (marked 0)
# The robot can pick up only one box at a time and once picked up 
# it has to return the box to the dropzone by moving onto the dropzone cell.
# Once the robot has stepped on the dropzone, the box is taken away, 
# and it is free to continue with its todo list.
# Tasks must be executed in the order that they are given in the todo list.
# You may assume that in all warehouse maps, all boxes are
# reachable from beginning (the robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works!)
# in a function named plan() that takes as input three parameters: 
# warehouse, dropzone, and todo. See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order, which should
# match with our answer. You may include print statements to show 
# the optimum path, but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
# 
# Add your code at line 76.
# 
# --------------------
# Parameter Info
#
# warehouse - a grid of values, where 0 means that the cell is passable,
# and a number 1 <= n <= 99 means that box n is located at that cell.
# dropzone - determines the robot's start location and the place to return boxes 
# todo - list of tasks, containing box numbers that have to be picked up
#
# --------------------
# Testing
#
# You may use our test function below, solution_check(),
# to test your code for a variety of input parameters. 

warehouse = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone = [2,0] 
todo = [2, 1]

def heiristics(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

# ------------------------------------------
# plan - Returns cost to take all boxes in the todo list to dropzone
#
# ----------------------------------------
# modify code below
# ----------------------------------------
def plan(warehouse, dropzone, todo):
    path_cost = 0
    
    actions = [
        [-1,  0], # up
        [-1,  1], # up-right
        [ 0,  1], # right
        [ 1,  1], # down-right
        [ 1,  0], # down
        [ 1, -1], # down-left
        [ 0, -1], # left
        [-1, -1]  # up-left
    ]

    costs = [
        1.0, # up
        1.5, # up-right
        1.0, # right
        1.5, # down-right
        1.0, # down
        1.5, # down-left
        1.0, # left
        1.5  # up-left
    ]

    symbols = [
        '^', # up
        '/', # up-right
        '>', # right
        '\\', # down-right
        'v', # down
        '/', # down-left
        '<', # left
        '\\'  # up-left
    ]

    for td in todo:
        for wr in range(len(warehouse)):
            for wc in range(len(warehouse[0])):
                if warehouse[wr][wc] == td:
                    goal = [wr, wc]
                    break

        print 'Planning a path from (%d, %d) to (%d, %d) [goal %d]' % (dropzone[0], dropzone[1], goal[0], goal[1], td)
        map = [[warehouse[row][col] for col in range(len(warehouse[0]))] for row in range(len(warehouse))]
        map[goal[0]][goal[1]] = '*'
        map[dropzone[0]][dropzone[1]] = 'x'
        for m in map:
            print m        

        r = dropzone[0]
        c = dropzone[1]
        g = 0
        f = g + heiristics(dropzone, goal)
        open = [[f, g, r, c]]
        action_map = [[9 for col in range(len(warehouse[0]))] for row in range(len(warehouse))]
        closed = [[0 for col in range(len(warehouse[0]))] for row in range(len(warehouse))]
        closed[r][c] = 1

        found = False
        resign = False
        while not found and not resign:
            if len(open) == 0:
                resign = True
                print 'Search finished without success'
            else:
                open.sort(reverse=True)
                cell = open.pop()
                r = cell[2]
                c = cell[3]
                g = cell[1]

                if r == goal[0] and c == goal[1]:
                    found = True
                else:
                    for i in range(len(actions)):
                        action = actions[i]
                        cost = costs[i]
                        r2 = r + action[0]
                        c2 = c + action[1]
                        if r2 >= 0 and r2 < len(warehouse) and c2 >= 0 and c2 < len(warehouse[0]):
                            if closed[r2][c2] == 0 and (warehouse[r2][c2] == 0 or warehouse[r2][c2] == td):
                                g2 = g + cost
                                h2 = heiristics([r2, c2], goal)
                                f2 = g2 + h2
                                open.append([f2, g2, r2, c2])
                                closed[r2][c2] = 1
                                action_map[r2][c2] = i

        print 'Found: %s' % found
        invpath = []
        r = goal[0]
        c = goal[1]
        invpath.append([r, c])

        print '### Action map ###'
        for row in action_map:
            print row

        while r != dropzone[0] or c != dropzone[1]:
            ai = action_map[r][c]
            action = actions[ai]
            r = r - action[0]
            c = c - action[1]
            path_cost += 2 * costs[ai]
            invpath.append([r, c, ai])

        invpath.reverse()

        print 'Path: ', invpath

        map = [[warehouse[row][col] for col in range(len(warehouse[0]))] for row in range(len(warehouse))]
        map[goal[0]][goal[1]] = '*'
        map[dropzone[0]][dropzone[1]] = 'x'
        
        for i in range(len(invpath) - 1):
            p = invpath[i]
            r = p[0]
            c = p[1]
            ai = p[2]
            map[r][c] = symbols[ai]

        print '### Path map ###'
        for m in map:
            print m

        warehouse[goal[0]][goal[1]] = 0    

    return path_cost
    
################# TESTING ##################
       
# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[]. Uncomment the call
# to solution_check to test your code.
#
def solution_check(test, epsilon = 0.00001):
    answer_list = []
    
    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i+1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            #print "#############################################"
        else:
            print "\nTest case ", i+1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost 
            answer_list.append(0)
    runtime =  time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False
#Testing environment
# Test Case 1 
warehouse1 = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone1 = [2,0] 
todo1 = [2, 1]
true_cost1 = 9
# Test Case 2
warehouse2 = [[   1, 2, 3, 4],
              [   0, 0, 0, 0],
              [   5, 6, 7, 0],
              [ 'x', 0, 0, 8]] 
dropzone2 = [3,0] 
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [[   1, 2,  3,  4, 5, 6,  7],
              [   0, 0,  0,  0, 0, 0,  0],
              [   8, 9, 10, 11, 0, 0,  0],
              [ 'x', 0,  0,  0, 0, 0, 12]] 
dropzone3 = [3,0] 
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[ 1, 17, 5, 18,  9, 19,  13],
              [ 2,  0, 6,  0, 10,  0,  14],
              [ 3,  0, 7,  0, 11,  0,  15],
              [ 4,  0, 8,  0, 12,  0,  16],
              [ 0,  0, 0,  0,  0,  0, 'x']] 
dropzone4 = [4,6]
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
                 [dropzone1, dropzone2, dropzone3, dropzone4],
                 [todo1, todo2, todo3, todo4],
                 [true_cost1, true_cost2, true_cost3, true_cost4]]


solution_check(testing_suite) #UNCOMMENT THIS LINE TO TEST YOUR CODE
