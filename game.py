import pygame
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 500
TILE_SIZE = 60
PLAYER = pygame.transform.scale(pygame.image.load('Icons\player1.png'), (TILE_SIZE, TILE_SIZE))
WALL = pygame.transform.scale(pygame.image.load('Icons\wall.png'), (TILE_SIZE, TILE_SIZE))
BOX = pygame.transform.scale(pygame.image.load('Icons\wall1.png'), (TILE_SIZE, TILE_SIZE))
TARGET = pygame.transform.scale(pygame.image.load('Icons\\target1.png'), (TILE_SIZE, TILE_SIZE))
BACKGROUND_COLOR = (200, 200, 200)

# Level design (a sample single level)
level = [
    "##########", 
    "#@       #",
    "##  $  $##",
    "#.      .#",
    "## $     ##",
    "#   #. # #",
    "##########"
]

player_pos = (1, 1)  # Starting position of the player

# Function to draw the level
def draw_level():
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            x_pos, y_pos = x * TILE_SIZE, y * TILE_SIZE
            if char == '#':
                screen.blit(WALL, (x_pos, y_pos))
            elif char == '@':
                screen.blit(PLAYER, (x_pos, y_pos))
            elif char == '$':
                screen.blit(BOX, (x_pos, y_pos))
            elif char == '.':
                screen.blit(TARGET, (x_pos, y_pos))

# Function to move the player and boxes
def move_player(dx, dy):
    global level, player_pos

    x, y = player_pos
    new_x, new_y = x + dx, y + dy

    # Check boundaries
    if not (0 <= new_x < len(level[0]) and 0 <= new_y < len(level)):
        return
    # Check for wall collision
    if level[new_y][new_x] != '#':
        # Update the player's position
        if level[new_y][new_x] == ' ' or level[new_y][new_x] == '.':
            if level[y][x] == '.':
                level[y] = level[y][:x] + '.' + level[y][x + 1:]
            else:
                level[y] = level[y][:x] + ' ' + level[y][x + 1:]
            if level[new_y][new_x] == '.':
                level[new_y] = level[new_y][:new_x] + '.' + level[new_y][new_x + 1:]
            else:
                level[new_y] = level[new_y][:new_x] + '@' + level[new_y][new_x + 1:]
            player_pos = (new_x, new_y)
        # Move the box if applicable
        elif level[new_y][new_x] == '$':
            box_new_x, box_new_y = new_x + dx, new_y + dy
            if level[box_new_y][box_new_x] == ' ' or level[box_new_y][box_new_x] == '.':
                if level[y][x] == '.':
                    level[y] = level[y][:x] + '.' + level[y][x + 1:]
                else:
                    level[y] = level[y][:x] + ' ' + level[y][x + 1:]
                if level[new_y][new_x] == '.':
                    level[new_y] = level[new_y][:new_x] + '.' + level[new_y][new_x + 1:]
                else:
                    level[new_y] = level[new_y][:new_x] + '@' + level[new_y][new_x + 1:]
                level[box_new_y] = level[box_new_y][:box_new_x] + '$' + level[box_new_y][box_new_x + 1:]
                player_pos = (new_x, new_y)
        
            
# Function to check if all boxes are on targets
def checkCorner():
    if(level[1][1]=='$' or level[1][8]=='$' or level[5][1]=='$' or level[5][8]=='$'):
        return True
    return False

def check_win():
    for row in level:
        if '.' in row:
            return False
    return True
# Main game loop
# ... (Previous code remains the same)
# Function to clear a specific area of the screen (where text was previously rendered)
# def clear_text(x, y, width, height):
#     pygame.draw.rect(screen, (0,0,0), (x, y, width, height))  # Fill the area with the background color

# Function to render text
# def render_text(text, x, y, font_size=36, color=(0,0,0)):
#     font = pygame.font.Font(None, font_size)
#     text_surface = font.render(text, True, color)
#     screen.blit(text_surface, (x, y))
# Function to render text at specific coordinates
def render_text(text, x, y, font_size=36, color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)  # Set the top-left corner of the text surface to the specified coordinates
    screen.blit(text_surface, text_rect.topleft)

# Main game loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
game_end = False  # Variable to track the game's winning state

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_level()

    if check_win():
        # Example usage to clear previously rendered text at coordinates (100, 150)
        # clear_text(100, 300, 2, 2)  # Replace text_width and text_height with the dimensions of the text rendered previously
        render_text("You win!", 230, 450)
        game_end = True
    if checkCorner():
        render_text("Block Cannot move ",180,450)
        game_end=True
    pygame.display.flip()

    if running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_end:  # Check if the game has not been won
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)
pygame.quit()