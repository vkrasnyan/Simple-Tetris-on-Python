import pygame
import random
import copy

# grid size
columns = 10
rows = 20

# screen size in pixels
screen_x = 250
screen_y = 500

# initialize Pygame
pygame.init()

# game window
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("MyTetris")

# object for tracking time
clock = pygame.time.Clock()

# cell parameters
cell_width = screen_x / columns
cell_height = screen_y / rows

# frames per second
fps = 60

# list for storing the grid
grid = []

for i in range(columns):
    grid.append([])
    for j in range(rows):
        grid[i].append([1])

for i in range(columns):
    for j in range(rows):
        grid[i][j].append(pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height))
        grid[i][j].append(pygame.Color("gray"))

# Tetris piece descriptions
details = [
    # line
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    # L-shaped
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    # reverse L-shaped
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    # square
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    # Z-shaped
    [[1, 0], [1, 1], [0, 0], [-1, 0]],
    # reverse Z-shaped
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    # T-shaped
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]


# function to create a new piece
def create_new_figure():
    detail_type = copy.deepcopy(random.choice(details))
    figure = [pygame.Rect(x * cell_width + screen_x // 2, y * cell_height, cell_width, cell_height) for x, y in
              detail_type]
    return figure


det_choice = create_new_figure()

# counter for tracking piece drop speed
count = 0
game = True
rotate = False

while game:
    # movement along the x-axis
    delta_x = 0
    # movement along the y-axis (falling)
    delta_y = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_x = -1
            elif event.key == pygame.K_RIGHT:
                delta_x = 1
            elif event.key == pygame.K_UP:
                rotate = True
    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN]:
        count = 31 * fps

    screen.fill(pygame.Color(127, 255, 212, 255))
    for i in range(columns):
        for j in range(rows):
            pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1], grid[i][j][0])

    # boundary and collision checks
    for i in range(4):
        if det_choice[i].x + delta_x * cell_width < 0 or det_choice[i].x + delta_x * cell_width >= screen_x:
            delta_x = 0
        if det_choice[i].y + cell_height >= screen_y or \
                grid[int(det_choice[i].x // cell_width)][int(det_choice[i].y // cell_height) + 1][0] == 0:
            delta_y = 0
            for i in range(4):
                x = int(det_choice[i].x // cell_width)
                y = int(det_choice[i].y // cell_height)
                grid[x][y][0] = 0
                grid[x][y][2] = pygame.Color("mediumorchid")
            det_choice = create_new_figure()
            break

    # move piece along x
    for i in range(4):
        det_choice[i].x += delta_x * cell_width
    count += fps
    if count >= 30 * fps:
        for i in range(4):
            det_choice[i].y += delta_y * cell_height
        count = 0

    # draw the piece
    for i in range(4):
        pygame.draw.rect(screen, pygame.Color("lightslateblue"), det_choice[i])

    # determine the center of the piece (third square in the list)
    C = det_choice[2]
    if rotate:
        for i in range(4):
            x = det_choice[i].y - C.y
            y = det_choice[i].x - C.x
            det_choice[i].x = C.x - x
            det_choice[i].y = C.y + y
        rotate = False

    # clear filled rows
    for j in range(rows - 1, -1, -1):
        count_cells = 0
        for i in range(columns):
            if grid[i][j][0] == 0:
                count_cells += 1
            elif grid[i][j][0] == 1:
                break
        if count_cells == columns:
            for k in range(j, 0, -1):
                for l in range(columns):
                    grid[l][k][0] = grid[l][k - 1][0]
                    grid[l][k][2] = grid[l][k - 1][2]
            for l in range(columns):
                grid[l][0][0] = 1
                grid[l][0][2] = pygame.Color("aqua")

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
