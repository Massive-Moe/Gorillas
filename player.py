import pygame
import math

class Player:
  def __init__(self, color, position, img):
    self.position = position
    self.img = img
    self.angle = 0
    self.power = 0
    self.color = color

  def update(self, mouse_pos):
    dx = mouse_pos[0] - self.position[0]
    dy = mouse_pos[1] - self.position[1]
    self.angle = math.atan2(dy, dx)
    self.power = min(math.hypot(dx, dy), 50)      
  
  def shoot(self, projectile):
    projectile.visible = True
    projectile.velocity = (
      math.cos(self.angle) * self.power, 
      math.sin(self.angle) * self.power
    )
    projectile.position = self.position

  def draw(self, display_surf):
    display_surf.blit(self.img, (self.position[0] - 23, self.position[1] - 35))
    #pygame.draw.circle(display_surf, self.color, self.position, 10)