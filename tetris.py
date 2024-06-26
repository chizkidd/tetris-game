import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 300, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Initialize grid
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Tetromino class
class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def draw(self, surface):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        pygame.Rect(
                            (self.x + col_index) * CELL_SIZE,
                            (self.y + row_index) * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE
                        )
                    )

    def move(self, dx, dy):
        if not self.check_collision(dx, dy, self.shape):
            self.x += dx
            self.y += dy

    def rotate(self):
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.check_collision(0, 0, new_shape):
            self.shape = new_shape

    def check_collision(self, dx, dy, shape):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    new_x = self.x + col_index + dx
                    new_y = self.y + row_index + dy
                    if (new_x < 0 or new_x >= GRID_WIDTH or
                        new_y < 0 or new_y >= GRID_HEIGHT or
                        grid[new_y][new_x]):
                        return True
        return False

    def lock(self):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid[self.y + row_index][self.x + col_index] = self.color
        clear_lines()

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    new_grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT - len(new_grid))] + new_grid
    grid = new_grid

def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(
                    surface,
                    grid[y][x],
                    pygame.Rect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )

def game_over():
    global running
    running = False
    print("Game Over")

# Main loop
running = True
clock = pygame.time.Clock()
current_tetromino = Tetromino(random.choice(SHAPES))
fall_time = 0
fall_speed = 500

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                current_tetromino.move(1, 0)
            elif event.key == pygame.K_DOWN:
                current_tetromino.move(0, 1)
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()

    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time >= fall_speed:
        fall_time = 0
        if current_tetromino.check_collision(0, 1, current_tetromino.shape):
            current_tetromino.lock()
            current_tetromino = Tetromino(random.choice(SHAPES))
            if current_tetromino.check_collision(0, 0, current_tetromino.shape):
                game_over()
        else:
            current_tetromino.move(0, 1)

    # Fill the background with black
    window.fill(BLACK)

    # Draw the grid
    draw_grid(window)

    # Draw current tetromino
    current_tetromino.draw(window)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
