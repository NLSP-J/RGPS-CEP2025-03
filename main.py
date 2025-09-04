import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
COLS, ROWS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 191, 255)
PURPLE = (160, 32, 240)

clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 24)
font = pygame.font.Font(None, 24)
# big_font = pygame.font.SysFont("Arial", 48)
big_font = pygame.font.Font(None, 48)

def reset_game():
    return {
        "snake": [(COLS//2, ROWS//2)],
        "direction": (0, -1),
        "fruit": spawn_fruit(),
        "fruit_type": random.choice(["normal", "gold", "blueberry"]),
        "power_up": spawn_power_up(),
        "score": 0,
        "game_over": False,
        "speed": 10,
        "teleporters": [((5, 5), (20, 20)), ((10, 25), (30, 5))]
    }

def spawn_fruit():
    return (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

def spawn_power_up():
    return (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

game = reset_game()

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*[c*TILE_SIZE for c in segment], TILE_SIZE, TILE_SIZE))

def draw_fruit(pos, fruit_type):
    color = RED if fruit_type == "normal" else GOLD if fruit_type == "gold" else PURPLE
    pygame.draw.rect(screen, color, (*[c*TILE_SIZE for c in pos], TILE_SIZE, TILE_SIZE))

def draw_power_up(pos):
    pygame.draw.rect(screen, BLUE, (*[c*TILE_SIZE for c in pos], TILE_SIZE, TILE_SIZE))

def draw_teleporters(pads):
    for a, b in pads:
        pygame.draw.rect(screen, WHITE, (*[c*TILE_SIZE for c in a], TILE_SIZE, TILE_SIZE), 2)
        pygame.draw.rect(screen, WHITE, (*[c*TILE_SIZE for c in b], TILE_SIZE, TILE_SIZE), 2)

def move_snake():
    head = game["snake"][0]
    new_head = ((head[0] + game["direction"][0]) % COLS,
                (head[1] + game["direction"][1]) % ROWS)
    game["snake"].insert(0, new_head)

    if new_head == game["fruit"]:
        if game["fruit_type"] == "normal":
            game["score"] += 1
        elif game["fruit_type"] == "gold":
            game["score"] += 5
        elif game["fruit_type"] == "blueberry":
            game["score"] += 3
        game["fruit"] = spawn_fruit()
        game["fruit_type"] = random.choice(["normal", "gold", "blueberry"])
    else:
        game["snake"].pop()

    if new_head == game["power_up"]:
        game["speed"] += 5
        game["power_up"] = spawn_power_up()

    for pad_a, pad_b in game["teleporters"]:
        if new_head == pad_a:
            game["snake"][0] = pad_b
        elif new_head == pad_b:
            game["snake"][0] = pad_a

    if new_head in game["snake"][1:]:
        game["game_over"] = True

def show_score():
    text = font.render(f"Score: {game['score']}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over_screen():
    screen.fill(BLACK)
    msg = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Your score: {game['score']}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

# Main Game Loop
running = True

def main():
    global running, game
    while running:
        clock.tick(game["speed"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game["game_over"]:
                    if event.key == pygame.K_UP and game["direction"] != (0, 1):
                        game["direction"] = (0, -1)
                    elif event.key == pygame.K_DOWN and game["direction"] != (0, -1):
                        game["direction"] = (0, 1)
                    elif event.key == pygame.K_LEFT and game["direction"] != (1, 0):
                        game["direction"] = (-1, 0)
                    elif event.key == pygame.K_RIGHT and game["direction"] != (-1, 0):
                        game["direction"] = (1, 0)
                else:
                    if event.key == pygame.K_r:
                        game = reset_game()
                    elif event.key == pygame.K_q:
                        running = False

        if not game["game_over"]:
            move_snake()
            screen.fill(BLACK)
            draw_snake(game["snake"])
            draw_fruit(game["fruit"], game["fruit_type"])
            draw_power_up(game["power_up"])
            draw_teleporters(game["teleporters"])
            show_score()
            pygame.display.flip()
        else:
            game_over_screen()

    pygame.quit()

main()