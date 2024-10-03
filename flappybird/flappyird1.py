# Importing the libraries
import pygame
import sys
import random

# Initializing pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()

# Function to draw the floor
def draw_floor():
    screen.blit(floor_img, (floor_x, height - floor_height))
    screen.blit(floor_img, (floor_x + floor_width, height - floor_height))

# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 250))  # Adjust the top pipe's position
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))  # Adjust the bottom pipe's position
    return top_pipe, bottom_pipe

# Function for pipe animation
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True

# Function to draw the score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, height - 120))
        screen.blit(high_score_text, high_score_rect)

# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score

# Game window (full screen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()  # Get the full screen size

# Set up background and base image
back_img = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/flappybird.png')
floor_img = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/floor.png')

# Scale the background and floor images
back_img = pygame.transform.scale(back_img, (width, height))  # Full-screen background
floor_width, floor_height = width, 100  # Resize the floor to fit the screen width
floor_img = pygame.transform.scale(floor_img, (floor_width, floor_height))

floor_x = 0

# Bird animation frames (scaled up)
bird_up = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/ang.png')
bird_down = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/ang.png')
bird_mid = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/ang.png')

# Scale up the bird images (increase size)
bird_up = pygame.transform.scale(bird_up, (45, 32))  # Increased size
bird_down = pygame.transform.scale(bird_down, (45, 32))
bird_mid = pygame.transform.scale(bird_mid, (45, 32))

birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(67, height // 2))
bird_movement = 0
gravity = 0.17

# Loading pipe image (smaller pipes)
pipe_img = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/pipe1.png')
pipe_img = pygame.transform.scale(pipe_img, (52, 300))  # Scale down the pipe image

pipe_height = [400, 350, 533, 490]

# Pipes setup
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1200)

# Game over setup
game_over = False
over_img = pygame.image.load('C:/Users/sarth/OneDrive/Desktop/AI club(Text to code)/flappybird/over.png')
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# Score variables
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Game loop
running = True
while running:
    clock.tick(120)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit event
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Key press event
            if event.key == pygame.K_SPACE and not game_over:  # Spacebar to jump
                bird_movement = 0
                bird_movement = -7

            if event.key == pygame.K_SPACE and game_over:  # Restart the game after game over
                game_over = False
                pipes = []
                bird_movement = 0
                bird_rect = bird_img.get_rect(center=(67, height // 2))
                score_time = True
                score = 0

        # Bird flap animation
        if event.type == bird_flap:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0
            bird_img = birds[bird_index]
            bird_rect = bird_up.get_rect(center=bird_rect.center)

        # Adding pipes
        if event.type == create_pipe:
            pipes.extend(create_pipes())

    # Background and floor drawing
    screen.blit(back_img, (0, 0))  # Full-screen background
    screen.blit(floor_img, (floor_x, height - floor_height))  # Floor at the bottom

    # Game over conditions
    if not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

        if bird_rect.top < 5 or bird_rect.bottom >= height - floor_height:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
    elif game_over:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    # Move the floor
    floor_x -= 1
    if floor_x < -floor_width:
        floor_x = 0

    draw_floor()

    # Update the screen
    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()
