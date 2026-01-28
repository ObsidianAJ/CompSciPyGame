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
        self.original_image = pygame.surface.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0,0,50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (self.centerx,self.centery))
        self.angle = 0
        self.rise = 10
        print(self.rect.topleft, self.rect.center)

    def aim(self, angle_delta):
        # if self.angle + angle_delta > 90 or self.angle + angle_delta < -90:
        #     pass
        # if:
        self.angle += angle_delta
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.centerx,self.centery))
        self.rect.center = (self.centerx,self.centery)
            # print(self.rect.topleft, self.rect.center)
            # print(self.angle)
        


    def move(self):
        BULLET_SPEED = 5
        angle_radians = math.radians(self.angle+90)
        vx = BULLET_SPEED * math.cos(angle_radians)
        vy = -BULLET_SPEED * math.sin(angle_radians)
        self.rect.centerx += vx
        self.rect.centery += vy
        self.centerx += vx
        self.centery += vy
        # if self.rect.left < 0 or self.rect.right>1200:
        #     return False
        # if self.rect.top < 0 or self.rect.bottom > 600:

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
                player.move()
                moving = True
    if moving == True:
        player.move()

    collisions = pygame.sprite.spritecollide(player, planets, False, pygame.sprite.collide_mask)
    grav_collisions = pygame.sprite.spritecollide(player, gravity_zones, False,pygame.sprite.collide_mask)

    for collided_planet in collisions:
        pass
        # running = False
    for grav_collided in grav_collisions:
        dx = gravity_zone.grav_x - player.centerx
        dy = gravity_zone.grav_y - player.centery
        target_angle_rad = math.atan2(dy, dx)
        target_angle_deg = math.degrees(target_angle_rad)

        # 2. Calculate the difference in angles
        angle_diff = target_angle_deg - player.angle

        # 3. Normalize the angle difference to find the shortest rotation direction
        # This ensures it turns the shorter way (e.g., from -170 to 170 degrees is a 20 degree turn, not 340)
        angle_diff = (angle_diff + 180) % 360 - 180

        # 4. Incrementally update the angle based on the rotation speed and direction
        if abs(angle_diff) > rotation_speed:
            if angle_diff > 0:
                # player.angle += rotation_speed
                player.aim(player.angle+rotation_speed)
            else:
                # player.angle -= rotation_speed
                player.aim(player.angle-rotation_speed)
        else:
            # If the difference is very small, just set it to the target angle to avoid jittering
            player.angle = target_angle_deg
        

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
