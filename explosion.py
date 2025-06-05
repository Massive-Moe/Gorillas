import pygame

class Explosion:
  def __init__(self, color):
    self.color = color
    self.timer = 0
    self.position = (0,0)

    Explosion.radius = 20
  
  def draw(self, display_surf):
    pygame.draw.circle(display_surf, self.color, self.position, Explosion.radius + self.timer*5)
