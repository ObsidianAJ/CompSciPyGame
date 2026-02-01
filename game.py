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
        self.grav_x =x
        self.grav_y = y
        self.image = pygame.surface.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,255), (radius, radius), radius)
        self.rect = self.image.get_rect(center = (self.grav_x,self.grav_y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.centerx = x
        self.centery = y
        self.vx = 0 
        self.vy = 0 
        self.rot_angle = 0
        self.original_image = pygame.surface.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0,0,50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (self.centerx,self.centery))
        self.angle = 0
        self.rise = 10
        print(self.rect.topleft, self.rect.center)

    def aim(self, angle_delta):
        self.angle += angle_delta
        self.rotate(angle_delta)


    def rotate(self, angle_delta): 
        self.rot_angle += angle_delta   
        self.image = pygame.transform.rotate(self.original_image, self.rot_angle)    
        self.rect = self.image.get_rect(center=(self.centerx,self.centery))
        self.rect.center = (self.centerx,self.centery)
        


    def move(self):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        self.centerx += self.vx
        self.centery += self.vy

class Win_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0,255,0), (radius, radius), radius)
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

planets = pygame.sprite.Group()
planets.add(Planet(300, 300,70))

gravity_zones = pygame.sprite.Group()
gravity_zone = Gravity(300,300,90)
gravity_zones.add(gravity_zone)

player = Player(400,550,(250,0,0))

win_zone = Win_Platform(350,50,30)


all = pygame.sprite.Group()
all.add(gravity_zones)
all.add(planets)
all.add(player)
all.add(win_zone)

# Main game loop
running = True
moving = False
rotation_speed = 1
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if moving == False:
            if keys[pygame.K_d]:
                player.aim(-1)
            if keys[pygame.K_a]:
                player.aim(1)
            if keys[pygame.K_SPACE]:
                moving = True
                BULLET_SPEED = 5
                angle_radians = math.radians(player.angle+90)
                player.vx = BULLET_SPEED * math.cos(angle_radians)
                player.vy = -BULLET_SPEED * math.sin(angle_radians)
    if moving == True:
        player.move()

    collisions = pygame.sprite.spritecollide(player, planets, False, pygame.sprite.collide_mask)
    grav_collisions = pygame.sprite.spritecollide(player, gravity_zones, False,pygame.sprite.collide_mask)

    for collided_planet in collisions:
        pass

    for grav_collided in grav_collisions:
        dx = grav_collided.rect.centerx - player.centerx
        dy = grav_collided.rect.centery - player.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            G_CONSTANT = 0.15
            player.vx += (dx / distance) * G_CONSTANT
            player.vy += (dy / distance) * G_CONSTANT
            player.rotate((player.vy/player.vx)/10)
        

        # Keep the angle within a standard range if needed
        player.angle %= 360
        if player.rect.colliderect(win_zone.rect):
            moving = False

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