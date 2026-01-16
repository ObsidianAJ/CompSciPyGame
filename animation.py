import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.index = 0
        self.direction = "right"
        self.x = x
        self.y = y
        self.right_jump_image = pygame.image.load("Base pack\Player\p3_jump.png").convert_alpha()
        self.stand_image = pygame.image.load("Base pack\Player\p3_front.png").convert_alpha()
        self.right_walk_images = [pygame.image.load(f"Base pack\Player\p3_walk\PNG\p3_walk{i}.png").convert_alpha() for i in range(1,12)]
        self.images = [[self.stand_image],[self.right_walk_images],[self.right_jump_image], [pygame.transform.flip(img, True, False) for img in self.right_walk_images], [pygame.transform.flip(self.right_jump_image, True, False)]]
        self.image = self.images[0][0]
        self.rect = self.image.get_rect(center = (x,y))
# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (60,60,60)

# Create clock to later control frame rate
clock = pygame.time.Clock()

player = Player(100,100)

all = pygame.sprite.Group()
all.add(player)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False


    # Fill the screen with a color (e.g., white)
    screen.fill(BLACK)
    all.draw(screen)







    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()