print ('rbna yshil isa')

import pygame
import random

pygame.font.init()

# Screen dimensions
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 50

# Shapes formats - just got these formats form the internet
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#putting all these shapes together in an array to be called later and assigning colours in a diff array 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


#class that will have all info about the shapes that will be used
class Piece:
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # here i am just creating the main clack grid that will be played on 20*10 black colour
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    # now this is a loop where the grid gets its current colour as the grid is a 2D list so its a nested for loop
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                # will get the colour of the locked position
                c = locked_positions[(j, i)]

                # then it will set the grid position to the colour of the locked position
                grid[i][j] = c
    return grid


# the function where shapes will change their formats
def convert_shape_format(shape):
    positions = []
    # list storing the positions of the shape's blocks
    
    format = shape.shape[shape.rotation % len(shape.shape)]
    # get the current rotation of the shape

    # itertaing over each line in the current rotation of the shape
    for i, line in enumerate(format):
        row = list(line)  # converting the line into a list of characters

        # iterating over each character in the row
        for j, column in enumerate(row):
            if column == '0':  # this means it represents a block in the shape

                # so append the position of the block in the grid
                positions.append((shape.x + j, shape.y + i))

    # this is just for adjustment 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# this fucntions goal is to determine the okay places to put shapes in, aka pace where it is black and no shapes are there
def valid_space(shape, grid):
    # puts them all together in a list
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    # gets the positions of the current shape in the grid
    formatted = convert_shape_format(shape)

    # here we just check through this loop
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:  # ignore positions above the grid
                return False
    return True

# function that is called after shape is put down to check whether the player lost or not
#checks by seeing if the position if latest shape is above the grid itself
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)  # creates a font object
    label = font.render(text, 1, color)  # renders the text onto a surface

    # calculates the position to center the text on the screen
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - (label.get_height() / 2)))



def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    
    #horizontal grid lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))

        #vertical grid lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0  # this is a counter used for cleared rows
    for i in range(len(grid) - 1, -1, -1):  # iterates from bottom to top
        row = grid[i]
        if (0, 0, 0) not in row:  
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  # remove the locked positions in the full row
                except:
                    continue

    # if a row has been cleared then we shift all the above rows one step down
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)  # create a font object
    label = font.render('Next Shape', 1, (255, 255, 255))  # rendering the 'Next Shape' text shown on the right

    # coordinates for drawing the next shape
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    # get the current rotation of the next shape
    format = shape.shape[shape.rotation % len(shape.shape)]

    # draw the next shape on the screen
    for i, line in enumerate(format):
        row = list(line)  # converts the line into a list of characters
        for j, column in enumerate(row):
            if column == '0':  # if the character is '0', it represents a block in the shape
                pygame.draw.rect(surface, shape.color, 
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    # Draw the 'Next Shape' label
    surface.blit(label, (sx + 10, sy - 30))



def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))  # fill the window with black color, the intial colour of start

    pygame.font.init()  # initialize the font module
    font = pygame.font.SysFont('comicsans', 60)  # create a font object
    label = font.render('Tetris', 1, (255, 255, 255))  # render the 'Tetris' title at the top

    # draw the 'Tetris' title centered at the top of the screen
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 30)  
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))  # renders the score

    # coordinates of whre the score is written and then draw it
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    # draw the grid with the current state of the game
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], 
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)


    # draw the grid lines and the border of the play area
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), 
                     (top_left_x, top_left_y, play_width, play_height), 5)



def main():
    locked_positions = {}  # dictionary to keep track of locked positions on the grid
    grid = create_grid(locked_positions)  

    change_piece = False  # flag to determine if we need to change the current piece
    run = True  # flag to keep the game running
    current_piece = get_shape()  # get the first shape
    next_piece = get_shape()  # get the next shape
    clock = pygame.time.Clock()  # create a clock object to manage time
    fall_time = 0  # initialize the fall time counter
    score = 0  # initialize the score

    while run:
        grid = create_grid(locked_positions)  # updates the grid with locked positions
        fall_speed = 0.27  # set the default fall speed for the pieces

        fall_time += clock.get_rawtime()  # increment the fall time by the time since the last tick
        clock.tick()  # updates the clock

        # Check if the piece should fall
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # check for events (keyboard inputs, window close, etc.)
        # all basics of tetris that we all know: right key goes right left key goes left and so on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        # position of current shape
        shape_pos = convert_shape_format(current_piece)

        # draw the current piece on the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # in case the pieces's place needs to be changed
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        
        draw_window(win, grid, score)
        
        draw_next_shape(next_piece, win)
        
        pygame.display.update()

        # calling the check lost fucntion to know if u can still play or not
        if check_lost(locked_positions):
            draw_text_middle("YOU LOST!", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


def main_menu():
    run = True  # flag to keep the main menu loop running
    while run:
        win.fill((0, 0, 0))  # the black colour for the window
        draw_text_middle('Press Any Key to Play', 60, (255, 255, 255), win)  # the start message at the beginning of the game
        pygame.display.update() 
        for event in pygame.event.get():  # a loop handling user events input 
            if event.type == pygame.QUIT:  # if the user closes the window
                run = False  # stop the loop
            if event.type == pygame.KEYDOWN:  # if any key is pressed
                main()  # starts the main game loop
    pygame.quit()  # quits the game when the loop ends


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')  

main_menu()  


           
