import pyautogui

## Get the position of the board
top_left = pyautogui.locateCenterOnScreen('reference_images/upper_left.png')
down_right = pyautogui.locateCenterOnScreen('reference_images/down_right.png')

## If pyautogui can't find the corners it warns the user to update the corner images
if top_left == None:
    print("\nsolverbot.py stopped, please update the corner images (upper_left.png and down_right.png) in the 'reference_images' directory")
    print("this error could occur if you resize the window")
    exit()

## Set the width and the height of the board
board_width = (down_right[0] - top_left[0])
board_height = (down_right[1] - top_left[1])

## Set the width and height of the boxes
box_width = int(board_width / 9)
box_height = int(board_height / 9)

## Find the numbers and the position of the numbers on the board
numbers = []
for number in range(1, 10):
    for location in pyautogui.locateAllOnScreen('reference_images/' + str(number) + '.png', region=(top_left[0], top_left[1], board_width, board_height)):
        point_loc = pyautogui.center(location)
        x = point_loc[0] - top_left[0]
        y = point_loc[1] - top_left[1]
        numbers.append([number, x, y])

## If pyautogui can't find the numbers it warns the user to update the number images
if len(numbers) == 0:
    print("\nsolverbot.py stopped, please update the number images (1.png, 2.png... ) in the 'reference_images' directory")
    print("this error could also occur if you resize the window")
    exit()

print(f"{len(numbers)} numbers found on the board")

## Generate the positions for the board
board = []
box_y = 0
for row in range(1, 10):
    box_x = 0
    box_y = (box_y + 1) + box_height
    for column in range(1, 10):
        box_x = (box_x + 1) + box_width
        column_data = [row, column, box_x - box_width, box_x, box_y - box_height, box_y]
        board.append(column_data)

## Check the positions
positions = []
for number_position in numbers:
    for board_position in board:
        if board_position[2] <= number_position[1] <= board_position[3] and board_position[4] <= number_position[2] <= board_position[5]:
            positions.append([number_position[0], board_position[0], board_position[1]])

## Generate an empty 9x9 board filled with zeroes
sudoku = [[0]*9 for x in range(9)]

## Instert the numbers on the board
for position in positions:
    number, row, column = position[0], position[1] - 1, position[2] - 1
    sudoku[row][column] = number

## Solving the board, finding "empty" boxes
def find_zero(board):
    for a in range(len(board)):
        for b in range(len(board[0])):
            if board[a][b] == 0:
                return(a, b)
    return None

## Find numbers that can be put in the box
def is_valid(board, number, position):
    y = position[0] // 3
    x = position[1] // 3
    for a in range(y * 3, y * 3 + 3):
        for b in range(x * 3, x * 3 + 3):
            if board[a][b] == number and (a, b) != position:
                return False
    
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False
    
    for i in range(len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    return True

## Solve the board with backtracking algorithm
def solve(board):
    search = find_zero(board)
    if not search:
        return True
    else:
        row, column = search
    
    for i in range(1, 10):
        if is_valid(board, i, (row, column)):
            board[row][column] = i 
            if solve(board):
                return True
            board[row][column] = 0

    return False

solve(sudoku)

## Get the starting point for the input
x = top_left[0] + int(box_width / 2)
y = top_left[1] + int(box_height / 2)

## Input the board with pyautogui
for row in range(9):
    for column in range(9):
        pyautogui.click(x, y)
        pyautogui.press(str(sudoku[row][column]))
        x += box_width
    x = top_left[0] + int(box_width / 2)
    y += box_height

print("Done!")