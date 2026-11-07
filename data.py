import pygame

screen_width = 900
screen_height = 700
background = (217, 113, 173)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)

fow = 180
rays_number = 11
ray_max_length = 400

brain = "HUMAN"

pause_click_time = 70

player_images = [
    pygame.image.load("assets/spaceship_blue_spritesheet_1.png"),
    pygame.image.load("assets/spaceship_blue_spritesheet_2.png"),
    pygame.image.load("assets/spaceship_blue_spritesheet_3.png"),
    pygame.image.load("assets/spaceship_blue_spritesheet_4.png"),
    pygame.image.load("assets/spaceship_blue_spritesheet_5.png")
]
player_img_number = 0
size = (player_images[0].get_width() * 3, player_images[0].get_height() * 3)
player_speed = 1.15
player = pygame.transform.scale(player_images[player_img_number // 20], size)
player_position = [screen_width // 2 - size[0] // 2, screen_height - 170]
player_position_default = [screen_width // 2 - size[0] // 2, screen_height - 170]
player_list = []

asteroid_images = [
    pygame.image.load("assets/asteroid_large_1.png"),
    pygame.image.load("assets/asteroid_large_2.png"),
    pygame.image.load("assets/asteroid_small_1.png"),
    pygame.image.load("assets/asteroid_small_2.png"),
    pygame.image.load("assets/asteroid_small_3.png"),
    pygame.image.load("assets/asteroid_small_4.png"),
]
asteroid_generation_time = 100 if brain != "AI" else 170

weapon_level = 1
bullets_speed = 2
bullet_size_x = 7
bullet_size_y = 15
bullets_generation_time = 200
bullets = []

