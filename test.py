import math
import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (60, 60, 60)
RED = (250, 0, 0)
GREEN = (0, 255, 0)

# Global variables for movement to be updated by gravity
player_vx = 0
player_vy = 0
BULLET_SPEED = 5
ROTATION_SPEED = 2 # Speed at which the player rotates towards the gravity source

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
        self.grav_x = x
        self.grav_y = y
        # The gravity zone can be invisible; size is for collision detection
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (self.grav_x,self.grav_y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.centerx = x
        self.centery = y
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0,0,50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (self.centerx,self.centery))
        self.angle = 0
        self.rise = 10

    def aim(self, angle_delta):
        self.angle += angle_delta
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.centerx,self.centery))
        # Keep the angle within a standard range
        self.angle %= 360

    def move(self):
        # Use the global variables updated by gravity logic
        global player_vx, player_vy
        self.rect.centerx += player_vx
        self.rect.centery += player_vy
        self.centerx += player_vx
        self.centery += player_vy

class Win_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect(center = (x,y))

# Initialize Pygame and give access to all the methods in the package
pygame.init()
# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

# Create clock to later control frame rate
clock = pygame.time.Clock()

planets = pygame.sprite.Group()
planets.add(Planet(300, 300, 70))

gravity_zones = pygame.sprite.Group()
# Increase the gravity zone radius to give the player more time to rotate
gravity_zone = Gravity(300, 300, 150) 
gravity_zones.add(gravity_zone)

player = Player(400, 550, RED)
win_zone = Win_Platform(350, 50, 30)

all_sprites = pygame.sprite.Group()
all_sprites.add(gravity_zones)
all_sprites.add(planets)
all_sprites.add(player)
all_sprites.add(win_zone)

# Main game loop
running = True
moving = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if moving == False:
        if keys[pygame.K_d]:
            player.aim(-2) # Slightly slower aiming
        if keys[pygame.K_a]:
            player.aim(2)
        if keys[pygame.K_SPACE]:
            # Set initial velocity when launching
            angle_radians = math.radians(player.angle + 90)
            player_vx = BULLET_SPEED * math.cos(angle_radians)
            # Pygame y-coordinates increase downwards, so we invert math.sin result
            player_vy = -BULLET_SPEED * math.sin(angle_radians) 
            moving = True
            print(f"Launched at angle {player.angle}, vx: {player_vx}, vy: {player_vy}")

    if moving == True:
        # Check for gravity collision first to apply force
        grav_collisions = pygame.sprite.spritecollide(player, gravity_zones, False, pygame.sprite.collide_mask)
        for grav_collided in grav_collisions:
            # Calculate the direction vector from the player to the center of the gravity source
            dx = gravity_zone.grav_x - player.centerx
            dy = gravity_zone.grav_y - player.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            # Apply a constant force/acceleration towards the center
            # Normalize the direction vector and scale by a gravity strength factor
            gravity_strength = 0.05 
            if distance != 0:
                player_vx += (dx / distance) * gravity_strength
                player_vy += (dy / distance) * gravity_strength
            
            # Orient the player sprite to follow the path (optional but helpful visual)
            # Calculate the current angle of movement
            movement_angle_rad = math.atan2(player_vy, player_vx)
            # Convert to degrees, adjusting for pygame's coordinate system (y-down) and rotation logic
            movement_angle_deg = math.degrees(movement_angle_rad) - 90 
            player.angle = movement_angle_deg
            player.image = pygame.transform.rotate(player.original_image, player.angle)
            player.rect = player.image.get_rect(center=(player.centerx, player.centery))

        # Move the player using the updated velocity
        player.move()

        # Check for planet collisions (lose condition)
        collisions = pygame.sprite.spritecollide(player, planets, False, pygame.sprite.collide_mask)
        for collided_planet in collisions:
            print("Collision with planet!")
            running = False # End game on collision

        # Check for win condition
        if player.rect.colliderect(win_zone.rect):
            print("You Win!")
            moving = False
            # You might want to add win logic here (e.g., reset game, next level, display message)

    # Fill the screen with a color (e.g., black)
    screen.fill(BLACK)
    all_sprites.draw(screen) # Use the correct group name
    # Update the display
    pygame.display.flip()
    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
