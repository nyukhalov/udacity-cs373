# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    rows = len(grid)
    cols = len(grid[0])
    
    change = True
    while change:
        change = False
        for row in range(rows):
            for col in range(cols):
                if row == goal[0] and col == goal[1]:
                    if value[row][col] > 0:
                        value[row][col] = 0
                        policy[row][col] = '*'
                        change = True
                
                elif grid[row][col] == 0:
                    for d in range(len(delta)):
                        row2 = row + delta[d][0]
                        col2 = col + delta[d][1]
                        if row2 >= 0 and row2 < rows and col2 >= 0 and col2 < cols and grid[row2][col2] == 0:
                            left_d = (d + 1) % len(delta)
                            right_d = (d - 1) % len(delta)
                        
                            left_row = row + delta[left_d][0]
                            left_col = col + delta[left_d][1]
                        
                            right_row = row + delta[right_d][0]
                            right_col = col + delta[right_d][1]
                        
                            if left_row >= 0 and left_row < rows and left_col >= 0 and left_col < cols:
                                left_value = value[left_row][left_col]
                            else:
                                left_value = collision_cost
                            
                            if right_row >= 0 and right_row < rows and right_col >= 0 and right_col < cols:
                                right_value = value[right_row][right_col]
                            else:
                                right_value = collision_cost                            
                            
                            v2 = cost_step + (success_prob * value[row2][col2]) + (failure_prob * left_value) + (failure_prob * right_value)
                        
                            if v2 < value[row][col]:
                                value[row][col] = v2
                                policy[row][col] = delta_name[d]
                                change = True
                            
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977], 
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738], 
#[700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
