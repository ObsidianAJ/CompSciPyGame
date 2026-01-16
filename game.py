import pygame
import sys

class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        # gravity = ravity(x,y,self.radius)
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (radius, radius), radius)
        self.rect = self.image.get_rect(center = (x,y))

        
class Gravity(pygame.sprite.Sprite) :
    def __init__(self,x ,y, radius):
        super().__init__()
        radius *= 2
        self.image = pygame.surface.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,255), (radius, radius), radius)
        self.rect = self.image.get_rect(center = (x,y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.original_image = pygame.Surface((40, 40))
        self.original_image.fill(color)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x,y))
        self.angle = 0

    def aim(self, angle_delta):
        self.angle += angle_delta
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


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
planets.add(Planet(300, 300,70))

gravity_zones = pygame.sprite.Group()
gravity_zones.add(Gravity(300,300,70))

player = Player(400,550,(250,25,250))

all = pygame.sprite.Group()
all.add(player)
all.add(gravity_zones)
all.add(planets)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.aim(-5)
        if keys[pygame.K_d]:
            player.aim(5)

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
