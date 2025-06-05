import pygame

import math

BALL_SPEED = 25
GRAVITY = 2

class Banana:
  def __init__(self, position, radius, img):
    self.position = position
    self.radius = radius
    self.velocity = (0, 0)
    self.visible = False
    self.rotation = 0
    self.image = pygame.transform.scale(img, (30, 30))
    self.image_copy = self.image.copy()
    self.rect = pygame.Rect(0, 0, (radius * 2) - 6, (radius * 2) - 6)
    self.update_rect()
  
  def update_rect(self):
    self.rect.x = self.position[0] - self.radius
    self.rect.y = self.position[1] - self.radius

  def update(self, dt):
    if not self.visible:
      return

    #Apply gravity to the ball
    self.position = (
      self.position[0] + self.velocity[0] * dt * BALL_SPEED, 
      self.position[1] + self.velocity[1] * dt * BALL_SPEED
    )
    self.velocity = (
      self.velocity[0],  
      self.velocity[1] + dt * BALL_SPEED * GRAVITY
    )

    #Must use a clean copy of the image so rotation looks correct
    self.rotation += (15 % 360) * math.copysign(1, -self.velocity[0])
    self.image = pygame.transform.rotate(self.image_copy, self.rotation)
    self.update_rect()
  
  def draw(self, display_surf):
    display_surf.blit(self.image, 
                       (self.position[0] - int(self.image.get_width() / 2),
                        self.position[1] - int(self.image.get_height() / 2))
                      )
    #pygame.draw.circle(display_surf, "orange", self.position, self.radius)