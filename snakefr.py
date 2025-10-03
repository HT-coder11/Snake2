import pygame
import pygwidgets
import sys
import random
import time

# Constants
FPS = 8
G = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
R = (255, 0, 0)
B = (150, 75, 0)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 840
CELL_SIZE = 30

def create_valid_wall(snake_body, snake_head, food_pos, existing_walls):
    max_cols = WINDOW_WIDTH // CELL_SIZE
    max_rows = WINDOW_HEIGHT // CELL_SIZE

    while True:
        # pick orientation: horizontal 2×1 or vertical 1×2
        if random.choice([True, False]):
            w_cells, h_cells = 2, 1
        else:
            w_cells, h_cells = 1, 2

        col = random.randrange(0, max_cols - w_cells + 1)
        row = random.randrange(0, max_rows - h_cells + 1)
        x, y = col * CELL_SIZE, row * CELL_SIZE

        # all grid cells this wall would occupy
        wall_cells = [
            (x + dx * CELL_SIZE, y + dy * CELL_SIZE)
            for dx in range(w_cells)
            for dy in range(h_cells)
        ]

        # ensure it doesn't overlap snake, food, or other walls
        bad = False
        for cx, cy in wall_cells:
            if [cx, cy] in snake_body or [cx, cy] == snake_head or [cx, cy] == food_pos:
                bad = True
                break
            for wx, wy, ww, wh in existing_walls:
                if wx <= cx < wx + ww and wy <= cy < wy + wh:
                    bad = True
                    break
            if bad:
                break

        if not bad:
            return [x, y], (w_cells * CELL_SIZE, h_cells * CELL_SIZE)
        # else loop again

def gameover(screen):
    font = pygame.font.SysFont('serif', 90)
    text = font.render("YOU DIED", True, R)
    rect = text.get_rect(midtop=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.5))
    screen.fill(BLACK)
    screen.blit(text, rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake McColdCheesy Man")
    clock = pygame.time.Clock()

    # Initial snake & food
    snake_head = [90, 90]
    snake_body = [[90, 90], [60, 90], [30, 90]]
    food_pos = [random.randrange(0, WINDOW_WIDTH, CELL_SIZE),
                random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)]
    score = 0
    score_text = pygwidgets.DisplayText(
        screen, (30, 20), f"Score: {score}", textColor=WHITE, fontSize=30
    )

    # Store walls as (x, y, w, h)
    walls = []

    direction = ""
    while True:
        # — Event handling —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != "down":
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                elif event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"

       
        if direction:
            if direction == "up":
                snake_head[1] -= CELL_SIZE
            elif direction == "down":
                snake_head[1] += CELL_SIZE
            elif direction == "right":
                snake_head[0] += CELL_SIZE
            elif direction == "left":
                snake_head[0] -= CELL_SIZE

            snake_body.insert(0, list(snake_head))

            # Eating food?
            if snake_head == food_pos:
                score += 1
                score_text.setValue(f"Score: {score}")

                # reposition food
                food_pos = [
                    random.randrange(0, WINDOW_WIDTH, CELL_SIZE),
                    random.randrange(0, WINDOW_HEIGHT, CELL_SIZE),
                ]
            else:
                snake_body.pop()

        
        target_walls = score // 2
        while len(walls) < target_walls:
            pos, size = create_valid_wall(snake_body, snake_head, food_pos, walls)
            walls.append((pos[0], pos[1], size[0], size[1]))

     
        screen.fill(BLACK)
        # snake body
        for seg in snake_body:
            pygame.draw.rect(
                screen, G,
                pygame.Rect(seg[0], seg[1], CELL_SIZE, CELL_SIZE)
            )
        # snake head
        pygame.draw.rect(
            screen, WHITE,
            pygame.Rect(snake_head[0], snake_head[1], CELL_SIZE, CELL_SIZE)
        )
        # food
        pygame.draw.rect(
            screen, R,
            pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)
        )
        # walls
        for wx, wy, ww, wh in walls:
            pygame.draw.rect(
                screen, B,
                pygame.Rect(wx, wy, ww, wh)
            )

    
        # with self
        for block in snake_body[1:]:
            if block == snake_head:
                gameover(screen)
        # with borders
        if (snake_head[0] < 0 or snake_head[0] >= WINDOW_WIDTH or
            snake_head[1] < 0 or snake_head[1] >= WINDOW_HEIGHT):
            gameover(screen)
        # with walls
        for wx, wy, ww, wh in walls:
            if wx <= snake_head[0] < wx + ww and wy <= snake_head[1] < wy + wh:
                gameover(screen)

        # draw score
        score_text.draw()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()


