from data import weapon_level, size, bullet_size_y, bullet_size_x, bullets_speed, screen_height, screen
import pygame
class Bullets:
    def __init__(self, player_pos):
        self.poses = []
        for i in range(weapon_level):
            x = size[0] * 2 // (weapon_level + 1) * (i + 1) - size[0] // 2 - bullet_size_x // 2 + player_pos[0]
            y = player_pos[1] - bullet_size_y
            self.poses.append([x, y])
        self.speed = bullets_speed
        self.bullet_color = (18, 255, 247)
        self.size = [bullet_size_x, bullet_size_y]

        self.draw_bullets()

    def draw_bullets(self):
        for pos in self.poses:
            bullet = pygame.Surface((self.size[0], self.size[1]))
            bullet.fill(self.bullet_color)
            screen.blit(bullet, pos)

    def update_bullets(self):
        i = 0
        while i < len(self.poses):
            self.poses[i][1] -= self.speed
            if self.poses[i][1] < 0 or self.poses[i][1] > screen_height:
                del self.poses[i]
                i -= 1
            i += 1

