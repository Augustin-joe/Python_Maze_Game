from enum import Enum
import random
import msvcrt
import time
import os

global maze
# Define maze dimensions (make it fit to your screen size)
num_row=14
num_columns=27
# Initialize maze grid
maze=[[0 for i in range(num_columns)]for j in range(num_row)]

# Initialize player position
current_row=0
current_col=0

# Initialize visited cells list
visited_cells=[[-1,-1]]
visited_rows=[0]
visited_cols=[0]

# Function to find a path through the maze
def find_path(current_row,current_col,visited_cells):

    # Helper function to choose a random item from a list
    def choose_random_item(next_possible_moves):
        return random.choice(next_possible_moves)
    same=True
    next_possible_moves=[[current_row+1,current_col],[current_row,current_col+1],[current_row-1,current_col],[current_row,current_col-1]]

    # Remove previously visited cells from available choices
    for x in visited_cells:
        if x in next_possible_moves:next_possible_moves.remove(x)

    # Checks the path is reached
    if current_row == num_row-1 and current_col == num_columns-1:
        return True
    else:
        if current_row==0:
            if [current_row-1,current_col] in next_possible_moves:next_possible_moves.remove([current_row-1,current_col])
        elif current_row==num_row-1:
            if [current_row+1,current_col] in next_possible_moves:next_possible_moves.remove([current_row+1,current_col])

        if current_col==0:
            if [current_row,current_col-1] in next_possible_moves:next_possible_moves.remove([current_row,current_col-1])
        elif current_col==num_columns-1:
            if [current_row,current_col+1] in next_possible_moves:next_possible_moves.remove([current_row,current_col+1])
    while same:
        if next_possible_moves:
            selected_choice = choose_random_item(next_possible_moves)
        else:
            return False
        current_row=selected_choice[0]
        current_col=selected_choice[1]
        same=False
        for n in range(len(visited_rows)):
            if visited_rows[n] == current_row and visited_cols[n]==current_col:
                same=True
                if [current_row,current_col] in next_possible_moves:next_possible_moves.remove([current_row,current_col])
                break
        
    visited_rows.append(current_row)
    visited_cols.append(current_col)

    # Recursive call to find next step in the find_path    
    def loop(current_row,current_col,visited_cells):
        return find_path(current_row,current_col,visited_cells)
    truce=loop(current_row,current_col,visited_cells)
    
    while truce==False:
        visited_cells.append([current_row,current_col])
        visited_rows.pop()
        visited_cols.pop()
        current_row=visited_rows[-1]
        current_col=visited_cols[-1]
        truce=loop(current_row,current_col,visited_cells)
    else:
        return True
    

# Call the find_path finding function
path_found=find_path(current_row,current_col,visited_cells)
game_table=[[[0,0,0,0] for i in range(num_columns)]for j in range(num_row)]

# Populate the game maze based on the path found
for i in range(len(visited_rows)):
    maze[visited_rows[i]][visited_cols[i]]=1

for i in range(len(visited_rows)-1):
    start_row=visited_rows[i]
    start_column=visited_cols[i]
    next_row=visited_rows[i+1]
    next_column=visited_cols[i+1]

    if start_row==next_row:
        if start_column<next_column:
            game_table[start_row][start_column][2]=1
            game_table[start_row][start_column+1][0]=1
        else:
            game_table[start_row][start_column][0]=1
            game_table[start_row][start_column-1][2]=1
    else:
        if start_row<next_row:
            game_table[start_row][start_column][3]=1
            game_table[start_row+1][start_column][1]=1
        else:
            game_table[start_row][start_column][1]=1
            game_table[start_row-1][start_column][3]=1

unexplored_cells=[]
explored_cells=[]

# Initialize unexplored_cells and explored_cells lists
for i in range(num_row):
    for j in range(num_columns):
        unexplored_cells.append([i,j])
for i in range(len(visited_rows)):
    if [visited_rows[i],visited_cols[i]] in unexplored_cells:unexplored_cells.remove([visited_rows[i],visited_cols[i]])
    explored_cells.append([visited_rows[i],visited_cols[i]])

# Function to find the next path
def explore_next_path(unexplored_cells,explored_cells):
    visited_cells=explored_cells
    next_path_rows=[]
    next_path_columns=[]

    # Function to find the next step in the path
    def next_path(current_row,current_column,visited_cells):

        def rand_number(next_possible_moves):
            return random.choice(next_possible_moves)
    
        next_possible_moves=[[current_row+1,current_column],[current_row,current_column+1],[current_row-1,current_column],[current_row,current_column-1]]

        # Remove previously visited cells from available choices
        for x in visited_cells:
            if x in next_possible_moves:next_possible_moves.remove(x)

        # Handle boundary cases
        if current_row==0:
            if [current_row-1,current_column] in next_possible_moves:next_possible_moves.remove([current_row-1,current_column])
        elif current_row==num_row-1:
            if [current_row+1,current_column] in next_possible_moves:next_possible_moves.remove([current_row+1,current_column])

        if current_column==0:
            if [current_row,current_column-1] in next_possible_moves:next_possible_moves.remove([current_row,current_column-1])
        elif current_column==num_columns-1:
            if [current_row,current_column+1] in next_possible_moves:next_possible_moves.remove([current_row,current_column+1])

        if next_possible_moves:
            selected_choice = rand_number(next_possible_moves)
        else:
            return visited_cells
        
        current_row=selected_choice[0]
        current_column=selected_choice[1]
        visited_cells.append(selected_choice)
        next_path_rows.append(current_row)
        next_path_columns.append(current_column)
        visited_cells=next_path(current_row,current_column,visited_cells)
        
        return visited_cells
          
    
    new_list=[]
    length=0
    num_unexplored_cells=len(unexplored_cells)

    # Loop through unexplored_cells list and find the next path
    while length< num_unexplored_cells:
            coordinates=unexplored_cells[length]
            current_row=coordinates[0]
            current_column=coordinates[1]
            condition_executed=False
            length+=1
    
            for no in range(len(explored_cells)):
            
                if explored_cells[no]==[current_row+1,current_column]:
                    next_path_rows.append(current_row)
                    next_path_columns.append(current_column)
                    visited_cells.append([current_row,current_column])
                    visited_cells = next_path(current_row,current_column,visited_cells)
                    new_list.append([current_row,current_column,3])
                    condition_executed=True
                    break
                elif explored_cells[no]==[current_row-1,current_column]:
                    next_path_rows.append(current_row)
                    next_path_columns.append(current_column)
                    visited_cells.append([current_row,current_column])
                    visited_cells = next_path(current_row,current_column,visited_cells)
                    new_list.append([current_row,current_column,1])
                    condition_executed=True
                    break
                elif explored_cells[no]==[current_row,current_column+1]:
                    next_path_rows.append(current_row)
                    next_path_columns.append(current_column)
                    visited_cells.append([current_row,current_column])
                    visited_cells = next_path(current_row,current_column,visited_cells)
                    new_list.append([current_row,current_column,2])
                    condition_executed=True
                    break
                elif explored_cells[no]==[current_row,current_column-1]:
                    next_path_rows.append(current_row)
                    next_path_columns.append(current_column)
                    visited_cells.append([current_row,current_column])
                    visited_cells = next_path(current_row,current_column,visited_cells)
                    new_list.append([current_row,current_column,0])
                    condition_executed=True
                    break
            #for looping diffrenet path and choosing start 
            if condition_executed:
                length=0
                for i in range(len(visited_cells)):
                    if visited_cells[i] in unexplored_cells:unexplored_cells.remove(visited_cells[i])
                num_unexplored_cells=len(unexplored_cells)
                
    for i in range(len(next_path_rows)-1):
        start_row=next_path_rows[i]
        start_column=next_path_columns[i]
        next_row=next_path_rows[i+1]
        next_column=next_path_columns[i+1]
        for x in new_list:
            if start_row==x[0] and start_column ==x[1]:
                game_table[start_row][start_column][x[2]]=1
                if x[2]==0:
                    game_table[start_row][start_column-1][2]=1
                elif x[2]==1:
                    game_table[start_row-1][start_column][3]=1
                elif x[2]==2:
                    game_table[start_row][start_column+1][0]=1
                elif x[2]==3:
                    game_table[start_row+1][start_column][1]=1
                break

        if start_row==next_row:
            if start_column<next_column:
                game_table[start_row][start_column][2]=1
                game_table[start_row][start_column+1][0]=1
            else:
                game_table[start_row][start_column][0]=1
                game_table[start_row][start_column-1][2]=1
        elif start_column==next_column:
            if start_row<next_row:
                game_table[start_row][start_column][3]=1
                game_table[start_row+1][start_column][1]=1
            else:
                game_table[start_row][start_column][1]=1
                game_table[start_row-1][start_column][3]=1
            
            
explore_next_path(unexplored_cells,explored_cells)

draw_horizontal=[["-" for i in range(num_columns)]for j in range(num_row+1)]
draw_vertical=[["|" for i in range(num_columns+1)]for j in range(num_row)]

for i in range(num_row):
    for j in range(num_columns):
        if game_table[i][j][1]==1:
            draw_horizontal[i][j]=" "
        if game_table[i][j][3]==1:
            draw_horizontal[i+1][j]=" "
        if game_table[i][j][0]==1:
            draw_vertical[i][j]=" "
        if game_table[i][j][2]==1:
            draw_vertical[i][j+1]=" "

def display_maze(player_position):

    for i in range(num_row):
        play_point=False
        if i==player_position[0]:
            play_point=True
        for j in range(num_columns):
            print(draw_horizontal[i][j]*6,end='')
        print()
        for j in range(num_columns):
            if play_point and j==player_position[1]:
                print(draw_vertical[i][j],end='  /\\ ')
            else:
                print(draw_vertical[i][j],end='     ')
        print("|")
        for j in range(num_columns):
            if play_point and j==player_position[1]:
                print(draw_vertical[i][j],end='  \\/ ')
            else:
                print(draw_vertical[i][j],end='     ')
        print("|")
    for j in range(num_columns):
        print("-"*6,end='')
    print()

# Define an Enum class for arrow keys
class ArrowKeys(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

def get_arrow_input(player_position):
    current_row=player_position[0]
    current_col=player_position[1]
    possible_moves=game_table[current_row][current_col]
    
    
    while True:
        val = 10
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow keys start with '\xe0'
            key = msvcrt.getch()
            if key == b'H':
                val = ArrowKeys.UP
            elif key == b'P':
                val = ArrowKeys.DOWN
            elif key == b'K':
                val = ArrowKeys.LEFT
            elif key == b'M':
                val = ArrowKeys.RIGHT
        else:
            pass
        if val != 10:
            if possible_moves[val.value] == 1:  # Use the enum value to index the possible_moves list
                if val == ArrowKeys.LEFT:
                    player_position = [current_row, current_col - 1]
                elif val == ArrowKeys.UP:
                    player_position = [current_row - 1, current_col]
                elif val == ArrowKeys.RIGHT:
                    player_position = [current_row, current_col + 1]
                elif val == ArrowKeys.DOWN:
                    player_position = [current_row + 1, current_col]
                return player_position     # Return the updated player position
        
game_running=True   
player_position=[0,0]
print("Use arrow keys to move")
print("                    /\\")
print("                    ||")
print("             <--          -->")
print("                    ||")
print("                    \\/")
time.sleep(3)
while game_running:
    os.system('cls')
    display_maze(player_position)
    player_position = get_arrow_input(player_position)
    if player_position==[num_row-1,num_columns-1]:
        game_running=False
        os.system('cls')
        display_maze(player_position)
        print("YOU WON")


