import pygame
import random
import sys
from pygame.locals import *

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT_SIZE = 22
GAME_TIME = 60  # seconds

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Recycle Marathon')
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# Load images
def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# Player sprite (Bin)
class Bin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('bin.png', (40, 60))
        self.rect = self.image.get_rect()

# Recyclable sprite
class Recyclable(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = load_image(img, (30, 30))
        self.rect = self.image.get_rect()

# Non-recyclable sprite
class NonRecyclable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('plastic.png', (40, 40))
        self.rect = self.image.get_rect()

# Create sprite groups
item_list = pygame.sprite.Group()
plastic_list = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create item sprites
recyclable_images = ["item1.png", "item2.png", "item3.png"]
for _ in range(50):
    item = Recyclable(random.choice(recyclable_images))
    item.rect.x = random.randrange(SCREEN_WIDTH)
    item.rect.y = random.randrange(SCREEN_HEIGHT)
    item_list.add(item)
    allsprites.add(item)

# Create plastic sprites
for _ in range(20):
    plastic = NonRecyclable()
    plastic.rect.x = random.randrange(SCREEN_WIDTH)
    plastic.rect.y = random.randrange(SCREEN_HEIGHT)
    plastic_list.add(plastic)
    allsprites.add(plastic)

# Create bin sprite
bin = Bin()
allsprites.add(bin)

# Initialize game variables
score = 0
start_time = pygame.time.get_ticks()
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)
timing_font = pygame.font.SysFont("Times New Roman", FONT_SIZE)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update game state
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000
    if elapsed_time >= GAME_TIME:
        if score > 50:
            screen.fill((0, 0, 0))
            text = font.render("Bin loot successful!", True, RED)
            screen.blit(text, (250, 40))
        else:
            screen.fill((0, 0, 0))
            text = font.render("Better luck next time", True, WHITE)
            screen.blit(text, (250, 40))
        pygame.display.update()
        pygame.time.wait(2000)
        break

    # Move bin
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        bin.rect.y -= 5
    if keys[pygame.K_DOWN]:
        bin.rect.y += 5
    if keys[pygame.K_LEFT]:
        bin.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        bin.rect.x += 5

    # Collision detection
    item_hit_list = pygame.sprite.spritecollide(bin, item_list, True)
    plastic_hit_list = pygame.sprite.spritecollide(bin, plastic_list, True)

    # Update score
    for _ in item_hit_list:
        score += 1
    for _ in plastic_hit_list:
        score -= 5

    # Draw everything
    screen.fill((0, 0, 0))
    screen.blit(load_image("bground.png"), (0, 0))
    count_down = timing_font.render("Time Left: " + str(int(GAME_TIME - elapsed_time)), True, WHITE)
    screen.blit(count_down, (20, 10))
    text = font.render("Score = " + str(score), True, WHITE)
    screen.blit(text, (20, 50))
    allsprites.draw(screen)

    # Update display
    pygame.display.update()
    clock.tick(30)

pygame.quit()