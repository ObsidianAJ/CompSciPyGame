import math
import pygame
import sys
alive = True


class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
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
        self.x = x
        self.y = y
        self.original_image = pygame.surface.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0,0,50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.angle = 0
        self.rise = 10
        print(self.rect.topleft, self.rect.center)

    def aim(self, angle_delta):
        if self.angle + angle_delta > 90 or self.angle + angle_delta < -90:
            pass
        else:
            self.angle += angle_delta
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=(self.x,self.y))
            self.rect.center = (self.x,self.y)
            print(self.rect.topleft, self.rect.center)
            print(self.angle)
        


    def move(self):
        BULLET_SPEED = 5
        angle_radians = math.radians(self.angle+90)
        vx = BULLET_SPEED * math.cos(angle_radians)
        vy = -BULLET_SPEED * math.sin(angle_radians) 
        self.rect.centerx += vx
        self.rect.centery += vy





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
gravity_zones.add(Gravity(300,300,90))

player = Player(400,550,(250,0,0))

all = pygame.sprite.Group()
all.add(gravity_zones)
all.add(planets)
all.add(player)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.aim(-5)
        if keys[pygame.K_a]:
            player.aim(5)
        if keys[pygame.K_SPACE]:
            player.move()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # event.pos contains the (x, y) coordinates of the click
            print(f"Mouse clicked at coordinates: {event.pos}")

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
