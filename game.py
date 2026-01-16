import pygame
import sys

class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 50
        self.gravity = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
        pygame.draw.circle(self.gravity, (0,0,150), (self.radius, self.radius), self.radius)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def gravity(self):
        pass
        

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

    def move(self, deltax, deltay):
        if self.rect.left < 0 or self.rect.right>1200:
            deltax *= -3
        if self.rect.top < 0 or self.rect.bottom > 600:
            deltay *= -3

        self.rect.centerx += deltax
        self.rect.centery += deltay





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

planets = pygame.sprite.Group()
planets.add(Planet(300, 300))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(BLACK)
    planets.draw(screen)







    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
