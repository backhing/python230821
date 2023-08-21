import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 300, 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHAPES_COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                 (0, 255, 255), (255, 165, 0), (128, 0, 128)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
GAME_SPEED = 500  # milliseconds per drop
FONT_SIZE = 36

# Initialize fonts
font = pygame.font.Font(None, FONT_SIZE)

# Initialize clock
clock = pygame.time.Clock()

# Initialize grid
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

def draw_block(x, y, color):
    pygame.draw.rect(DISPLAY, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x, y, SHAPES_COLORS[cell])

def collide(tetromino, x, y):
    for row_idx, row in enumerate(tetromino):
        for col_idx, cell in enumerate(row):
            if cell:
                if (
                    x + col_idx < 0 or x + col_idx >= GRID_WIDTH or
                    y + row_idx >= GRID_HEIGHT or grid[y + row_idx][x + col_idx]
                ):
                    return True
    return False

def clear_lines():
    lines_to_clear = [i for i, row in enumerate(grid) if all(row)]
    for line in lines_to_clear:
        grid.pop(line)
        grid.insert(0, [0] * GRID_WIDTH)

def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    DISPLAY.blit(text_surface, (x, y))

def main():
    global grid
    tetromino = random.choice(SHAPES)
    tetromino_x = GRID_WIDTH // 2 - len(tetromino[0]) // 2
    tetromino_y = 0
    game_over = False
    score = 0
    level = 1

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not collide(tetromino, tetromino_x - 1, tetromino_y):
                        tetromino_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not collide(tetromino, tetromino_x + 1, tetromino_y):
                        tetromino_x += 1
                elif event.key == pygame.K_DOWN:
                    if not collide(tetromino, tetromino_x, tetromino_y + 1):
                        tetromino_y += 1
                elif event.key == pygame.K_UP:
                    rotated_tetromino = list(zip(*tetromino[::-1]))
                    if not collide(rotated_tetromino, tetromino_x, tetromino_y):
                        tetromino = rotated_tetromino

        if not collide(tetromino, tetromino_x, tetromino_y + 1):
            tetromino_y += 1
        else:
            for row_idx, row in enumerate(tetromino):
                for col_idx, cell in enumerate(row):
                    if cell:
                        grid[tetromino_y + row_idx][tetromino_x + col_idx] = cell
            clear_lines()
            tetromino = random.choice(SHAPES)
            tetromino_x = GRID_WIDTH // 2 - len(tetromino[0]) // 2
            tetromino_y = 0

            score += 10
            if score >= level * 100:
                level += 1
                pygame.time.set_timer(pygame.USEREVENT, GAME_SPEED // level)

            if collide(tetromino, tetromino_x, tetromino_y):
                game_over = True

        DISPLAY.fill(BLACK)
        draw_grid()
        for row_idx, row in enumerate(tetromino):
            for col_idx, cell in enumerate(row):
                if cell:
                    draw_block(tetromino_x + col_idx, tetromino_y + row_idx, SHAPES_COLORS[cell])
        draw_text(f"Score: {score}", 10, 10, WHITE)
        draw_text(f"Level: {level}", WIDTH - 120, 10, WHITE)

        pygame.display.update()
        clock.tick(3)

    pygame.quit()

if __name__ == "__main__":
    main()
