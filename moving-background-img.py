import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_SPEED = 2

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the background image (add your image file path)
background = pygame.image.load("./img/dark-yellow2-road.png")

# This is to make sure the image fits in the screen. You can skip this if your image size matches the screen size
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Initial position of the background
y = 0

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the background
    y += BACKGROUND_SPEED
    if y >= HEIGHT:
        y = 0

    # Draw the background twice to create the continuous scrolling effect
    screen.blit(background, (0, y))
    screen.blit(background, (0, y - HEIGHT))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
