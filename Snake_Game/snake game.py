import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (227, 250, 252)
red = (255, 0, 0)
green = (6, 138, 8)
light_green = (41, 43, 41)  # light green for snake head
dark_green = (144, 238, 144)  # dark green for snake tail
black = (0, 0, 0)
blue = (0, 0, 255)

# Fonts
font_style = pygame.font.SysFont(None, 30)

# Default settings
default_volume = 0.5
default_snake_speed = 10
default_sound_on = False
default_level = "Easy"

# Current settings
volume = default_volume
snake_speed = default_snake_speed
sound_on = default_sound_on
level = default_level

# load the logo image
logo = pygame.image.load("logo.png")

# Set the logo as the taskbar icon
pygame.display.set_icon(logo)


# Sounds (placeholders)
try:
    script_dir = os.path.dirname(__file__)

    # Load sound files
    eating_sound = pygame.mixer.Sound(os.path.join(script_dir, "eat_sound.wav"))
    collision_sound = pygame.mixer.Sound(os.path.join(script_dir, "collision_sound.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(script_dir, "game_over_sound.wav"))
    pygame.mixer.music.load(os.path.join(script_dir, "background_music.wav"))
    pygame.mixer.music.set_volume(volume)  # Set default volume
    #if sound_on:
     #   pygame.mixer.music.play(-1)  # Play background music indefinitely
except FileNotFoundError:
    print("Error: Sound files not found!")
    sys.exit()



# Function to display message on screen
def message(msg, color, y_displace=0):
    msg_display = font_style.render(msg, True, color)
    text_rect = msg_display.get_rect(center=(width / 2, height / 3 + y_displace))
    screen.blit(msg_display, text_rect)

# Function to create buttons
def draw_button(msg, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    button_text = font_style.render(msg, True, white)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)

# Function to handle button click
def is_button_clicked(x, y, button_rect):
    return button_rect.collidepoint(x, y)

# Function to draw the snake with gradient color
def draw_snake(block_size, snake_list):
    for i, (x, y) in enumerate(snake_list):
        # Calculate color based on position in snake list
        r = dark_green[0] + (light_green[0] - dark_green[0]) * i / len(snake_list)
        g = dark_green[1] + (light_green[1] - dark_green[1]) * i / len(snake_list)
        b = dark_green[2] + (light_green[2] - dark_green[2]) * i / len(snake_list)
        color = (r, g, b)
        pygame.draw.rect(screen, color, [x, y, block_size, block_size])


# Function to display game over screen
def game_over_screen(score):
    screen.fill(white)
    message("Game Over!", red, -50)
    message("Your Score: " + str(score), red, 50)
    draw_button("Main Menu", green, 150, 350, 150, 50)
    draw_button("Quit", red, 340, 350, 150, 50)
    pygame.display.update()

    # Define main menu button rectangle
    main_menu_button_rect = pygame.Rect(150, 350, 150, 50)
    quit_button_rect = pygame.Rect(340, 350, 150, 50)  # Define quit button rectangle
    # Play game over sound
    if sound_on:
        game_over_sound.set_volume(volume)
        game_over_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if is_button_clicked(x, y, main_menu_button_rect):
                    return "main_menu"
                elif is_button_clicked(x, y, quit_button_rect):
                    pygame.quit()
                    sys.exit()

# Function to handle settings
def handle_settings():
    global volume, snake_speed, sound_on, level

    while True:
        screen.fill(white)
        message("Settings", red, -130)
        
        # Volume slider
        pygame.draw.rect(screen, black, (150, 150, 400, 40), 3)  # Slider track
        pygame.draw.circle(screen, black, (int(150 + volume * 400), 170), 10)  # Slider button
        message(f"Volume: {int(volume * 100)}%", black, -40)
        
        # Sound toggle button
        if sound_on:
            draw_button("Sound: ON", green, 150, 220, 160, 40)
        else:
            draw_button("Sound: OFF", red, 150, 220, 160, 40)
        
        # Game level selection
        draw_button(f"Game Level: {level}", blue, 150, 290, 220, 40)
        
        # Back button
        draw_button("Back", green, 280, 350, 80, 40)  # Add Back button
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 550 and 150 <= y <= 190:
                    # Adjust volume based on mouse position
                    volume = max(0, min(1, (x - 150) / 400))
                    pygame.mixer.music.set_volume(volume)
                    eating_sound.set_volume(volume)
                    collision_sound.set_volume(volume)
                    game_over_sound.set_volume(volume)
                elif 150 <= x <= 310 and 220 <= y <= 260:
                    # Toggle sound on/off
                    sound_on = not sound_on
                    if sound_on:
                        #pygame.mixer.music.unpause()  # Unpause music when sound is on
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.pause()  # Pause music when sound is off
                elif 150 <= x <= 370 and 290 <= y <= 330:
                    # Cycle through game levels
                    if level == "Easy":
                        level = "Medium"
                        snake_speed = 15
                    elif level == "Medium":
                        level = "Hard"
                        snake_speed = 20
                    else:
                        level = "Easy"
                        snake_speed = 10
                elif 280 <= x <= 360 and 350 <= y <= 390:
                    return  # Return to main menu

# Main menu function
def main_menu():
    while True:
        screen.fill(white)
        message("Welcome to Snake Game!", red, -130)
        message("Instructions:", black, -100)
        message("- Use arrow keys to move the snake.", black, -70)
        message("- Eat the food to grow longer.", black, -40)
        message("- Avoid colliding with walls or yourself.", black, -10)
        message("- Press the Space key to pause between the game.", black, 20)
        message("- Press Start new game to start the game.", black, 50)
        draw_button("Settings", blue, 220, 300, 200, 40)  # Add Settings button
        draw_button("Start New Game", green, 220, 250, 200, 40)
        draw_button("Quit", red, 280, 350, 80, 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    return "new_game"
                elif event.key == pygame.K_ESCAPE:  # Escape key
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 220 <= x <= 420 and 300 <= y <= 340:
                    handle_settings()
                elif 220 <= x <= 420 and 250 <= y <= 290:
                    return "new_game"
                elif 280 <= x <= 360 and 350 <= y <= 390:
                    pygame.quit()
                    sys.exit()

# Function to run the game
def run_game():
    block_size = 10  # Define block size
    global snake_speed

    game_over = False
    game_close = False
    paused = False

    # Initialize the snake position and length
    snake_list = []
    snake_length = 1

    # Initial position of snake
    x1 = width / 2
    y1 = height / 2

    # Movement variables
    x1_change = 0
    y1_change = 0

    # Position of food
    foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    # Score tracking
    score = 0

    # Main game loop
    while not game_over:
        while game_close:
            option = game_over_screen(score)
            if option == "main_menu":
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:  # Restrict left movement when moving right
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:  # Restrict right movement when moving left
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:  # Restrict upward movement when moving downward
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:  # Restrict downward movement when moving upward
                    y1_change = block_size
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if paused:
            message("Game is paused, To continue press Space", red, 0)
            pygame.display.update()
            continue

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            # Play collision sound
            if sound_on:
                collision_sound.play()
            game_close = True

        screen.fill(white)
        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])
        draw_snake(block_size, snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            snake_length += 1
            score += 10
            if sound_on:
                eating_sound.play()

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                # Play collision sound
                if sound_on:
                    collision_sound.play()
                game_close = True

        clock = pygame.time.Clock()
        clock.tick(snake_speed)

    # Play game over sound
    if sound_on:
        game_over_sound.play()

# Main menu loop
def game_loop():
    while True:
        option = main_menu()
        if option == "new_game":
            run_game()

# Start the game
game_loop()
