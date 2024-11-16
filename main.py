import pygame
import random
import sys

if __name__ == "__main__":
    pygame.init()


color = (16, 176, 59)
resolution = (640, 428)
grid_size = 20
icon = pygame.image.load("assets/logo.png")
apple = pygame.image.load("assets/apple.png")
apple = pygame.transform.scale(apple, (20, 20))


backgrounds = [
    pygame.image.load("assets/background1.png"),
    pygame.image.load("assets/background2.png"),
    pygame.image.load("assets/background3.png"),
    pygame.image.load("assets/background4.png"),
]


pygame.mixer.init()
background_music = pygame.mixer.music.load("assets/background_music.wav")
apple_sound = pygame.mixer.Sound("assets/apple_sound.mp3")
death_sound = pygame.mixer.Sound("assets/death_sound.mp3")


sprite_sheet = pygame.image.load("assets/Textures.png")


def get_texture(x, y):
    """
    Retrieves a section of the sprite sheet based on the given coordinates.

    Args:
    x (int): The x-coordinate of the desired texture.
    y (int): The y-coordinate of the desired texture.

    Returns:
    pygame.Surface: A surface containing the texture.
    """
    cell_width = 384
    cell_height = 384
    return sprite_sheet.subsurface(
        pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
    )


head_texture = get_texture(0, 0)
body_texture = get_texture(1, 0)
tail_texture = get_texture(2, 1)
eye_texture = get_texture(2, 0)


snake_size = 20
head_texture = pygame.transform.scale(head_texture, (snake_size, snake_size))
body_texture = pygame.transform.scale(body_texture, (snake_size, snake_size))
tail_texture = pygame.transform.scale(tail_texture, (snake_size, snake_size))
eye_texture = pygame.transform.scale(eye_texture, (snake_size // 2, snake_size // 2))


def draw_snake(screen, snake_body):
    """
    Draws the snake on the screen based on its body segments.

    Args:
    screen (pygame.Surface): The screen to draw the snake on.
    snake_body (list): A list of positions representing the snake's body.
    """
    for i, segment in enumerate(snake_body):
        if i == 0:

            screen.blit(head_texture, (segment[0], segment[1]))
            screen.blit(eye_texture, (segment[0] + 6, segment[1] + 6))
        elif i == len(snake_body) - 1:

            screen.blit(tail_texture, (segment[0], segment[1]))
        else:

            screen.blit(body_texture, (segment[0], segment[1]))


def draw_start_menu(screen):
    """
    Draws the start menu, including the game title and start/quit options.

    Args:
    screen (pygame.Surface): The screen to draw the menu on.
    """
    screen.fill((107, 63, 160))
    font = pygame.font.SysFont("comicsansms", 60, bold=True)
    title_text = font.render("Purple Serpent", True, (255, 255, 255))

    screen.blit(title_text, (resolution[0] // 2 - title_text.get_width() // 2, 30))

    font = pygame.font.SysFont("comicsansms", 40, bold=True)
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    start_text_rect = start_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 + 10)
    )
    quit_text_rect = quit_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 + 100)
    )

    pygame.draw.rect(screen, (255, 255, 255), start_text_rect.inflate(20, 20), 5)
    pygame.draw.rect(screen, (255, 255, 255), quit_text_rect.inflate(20, 20), 5)

    screen.blit(start_text, start_text_rect)
    screen.blit(quit_text, quit_text_rect)

    pygame.display.update()


def draw_difficulty_menu(screen):
    """
    Draws the difficulty selection menu.

    Args:
    screen (pygame.Surface): The screen to draw the difficulty menu on.
    """
    screen.fill((107, 63, 160))
    font = pygame.font.SysFont("comicsansms", 60, bold=True)
    title_text = font.render("Select Difficulty", True, (255, 255, 255))

    screen.blit(title_text, (resolution[0] // 2 - title_text.get_width() // 2, 30))

    font = pygame.font.SysFont("comicsansms", 40, bold=True)
    easy_text = font.render("1. Easy", True, (255, 255, 255))
    medium_text = font.render("2. Medium", True, (255, 255, 255))
    hard_text = font.render("3. Hard", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    easy_text_rect = easy_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 - 50)
    )
    medium_text_rect = medium_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 + 20)
    )
    hard_text_rect = hard_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 + 90)
    )
    quit_text_rect = quit_text.get_rect(
        center=(resolution[0] // 2, resolution[1] // 2 + 160)
    )

    pygame.draw.rect(screen, (255, 255, 255), easy_text_rect.inflate(20, 20), 5)
    pygame.draw.rect(screen, (255, 255, 255), medium_text_rect.inflate(20, 20), 5)
    pygame.draw.rect(screen, (255, 255, 255), hard_text_rect.inflate(20, 20), 5)
    pygame.draw.rect(screen, (255, 255, 255), quit_text_rect.inflate(20, 20), 5)

    screen.blit(easy_text, easy_text_rect)
    screen.blit(medium_text, medium_text_rect)
    screen.blit(hard_text, hard_text_rect)
    screen.blit(quit_text, quit_text_rect)

    pygame.display.update()


def select_difficulty():
    """
    Handles the selection of difficulty using keyboard input.

    Returns:
    str: The selected difficulty ("EASY", "MEDIUM", or "HARD").
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    return "EASY"
                if event.key == pygame.K_2:
                    return "MEDIUM"
                if event.key == pygame.K_3:
                    return "HARD"


def start_game(screen, difficulty):
    """
    Starts and runs the game loop, handling game mechanics such as snake movement, collision detection, and scoring.

    Args:
    screen (pygame.Surface): The screen to render the game.
    difficulty (str): The selected difficulty level ("EASY", "MEDIUM", or "HARD").

    Returns:
    int: The final score after the game ends.
    """
    global is_run
    is_run = True
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    change_to = direction
    score = 0
    applex = random.randint(0, (resolution[0] // grid_size - 1)) * grid_size
    appley = random.randint(0, (resolution[1] // grid_size - 1)) * grid_size

    pygame.mixer.music.play(-1, 0.0)

    background = random.choice(backgrounds)
    background = pygame.transform.scale(background, resolution)

    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()

    if difficulty == "EASY":
        move_delay = 120
    elif difficulty == "MEDIUM":
        move_delay = 80
    else:
        move_delay = 40

    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_UP:
                    change_to = "UP"
                if event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        if pygame.time.get_ticks() - last_move_time >= move_delay:
            last_move_time = pygame.time.get_ticks()

            if direction == "UP":
                snake_pos[1] -= grid_size
            if direction == "DOWN":
                snake_pos[1] += grid_size
            if direction == "LEFT":
                snake_pos[0] -= grid_size
            if direction == "RIGHT":
                snake_pos[0] += grid_size

            snake_pos[0] = snake_pos[0] // grid_size * grid_size
            snake_pos[1] = snake_pos[1] // grid_size * grid_size

            snake_body.insert(0, list(snake_pos))

            if snake_pos[0] == applex and snake_pos[1] == appley:
                score += 10
                apple_sound.play()
                applex = random.randint(0, (resolution[0] // grid_size - 1)) * grid_size
                appley = random.randint(0, (resolution[1] // grid_size - 1)) * grid_size
            else:
                snake_body.pop()

            if (
                snake_pos[0] >= resolution[0]
                or snake_pos[0] < 0
                or snake_pos[1] >= resolution[1]
                or snake_pos[1] < 0
            ):
                pygame.mixer.music.stop()
                death_sound.play()
                return score
            for block in snake_body[1:]:
                if block == snake_pos:
                    pygame.mixer.music.stop()
                    death_sound.play()
                    return score

        screen.fill(color)
        screen.blit(background, (0, 0))

        draw_snake(screen, snake_body)
        screen.blit(apple, (applex, appley))

        font = pygame.font.SysFont("comicsansms", 30, bold=True)
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))

        screen.blit(score_text, (10, 10))

        pygame.display.update()

        clock.tick(60)

    return True


def game_loop():
    """
    Runs the game loop, initializing the start menu, difficulty selection, and game loop.
    """
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Purple Serpent")
    pygame.display.set_icon(icon)

    draw_start_menu(screen)
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False

    while True:
        draw_difficulty_menu(screen)

        difficulty = select_difficulty()

        if not start_game(screen, difficulty):

            continue


game_loop()
