import pygame
import random
import math

import player
import banana
import explosion
from utils import circle_collision
from button import Button

EXPLOSION_RADIUS = 20

class Game:
  def __init__(self, screen, channel):
    self.screen = screen
    self.channel = channel

    Game.BANANA_IMG = pygame.image.load("banana.png").convert_alpha()
    Game.BANANA_IMG = pygame.transform.scale(Game.BANANA_IMG, (30,30))
    Game.GORILLA_BLUE_IMG = pygame.image.load('gorilla_blue.png').convert_alpha()
    Game.GORILLA_BLUE_IMG = pygame.transform.scale(Game.GORILLA_BLUE_IMG, (45,45))
    Game.GORILLA_RED_IMG = pygame.image.load('gorilla_red.png').convert_alpha()
    Game.GORILLA_RED_IMG = pygame.transform.scale(Game.GORILLA_RED_IMG, (45,45))

    Game.EXPLOSION_SOUND = pygame.mixer.Sound("explosion.mp3")
    Game.THROW_SOUND = pygame.mixer.Sound("throw.mp3")

    Game.wall_colors = [(200, 200, 200), (80, 80, 80)]

    self.game_over = -1
  
  def setup_game(self):
    wall_widths = [60]*6 + [80]*2 + [40]*3
    random.shuffle(wall_widths)

    self.holes = []

    x = 0
    self.wall_rects = []
    for width in wall_widths:
      self.wall_rects.append(pygame.Rect(
        x,
        random.randint(100,400),
        width,
        self.screen.get_height()
      ))
      x += width
    
    self.players = [
      player.Player((60, 77, 138), (self.wall_rects[0].width/2, self.wall_rects[0].y-10), Game.GORILLA_BLUE_IMG),
      player.Player((145, 45, 50), (self.screen.get_width() - self.wall_rects[-1].width/2, self.wall_rects[-1].y-10), Game.GORILLA_RED_IMG)
    ]
    
    self.banana = banana.Banana((0,0), 15, Game.BANANA_IMG)
    self.explosion = explosion.Explosion((255, 0, 0))

    self.active_player = 0
    self.game_over = -1

  def update(self, dt):
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_just_pressed()

    self.players[self.active_player].update(mouse_pos)
    if mouse_clicked[0] and not self.banana.visible:
      self.players[self.active_player].shoot(self.banana)
      self.channel.play(Game.THROW_SOUND)
    
    self.banana.update(dt)
    self.explosion.timer -= dt

    hit = self.check_collisions()

    if hit:
      self.banana.visible = False
      self.explosion.position = self.banana.position
      self.explosion.timer = 1
      
      self.banana.position = (-50, -50)
      self.banana.update_rect()
      self.active_player = (self.active_player + 1) % 2
      self.channel.play(Game.EXPLOSION_SOUND)
  
  def check_collisions(self):
    for i, player in enumerate(self.players):
      if i == self.active_player:
        continue

      if circle_collision(self.banana.position, player.position, self.banana.radius, 10):
        #print(f"Player {self.active_player} hit player {i}")
        self.game_over = self.active_player
        return True
    
    for hole in self.holes:
      if circle_collision(self.banana.position, hole, self.banana.radius, EXPLOSION_RADIUS - self.banana.radius):
        return False
    
    for wall in self.wall_rects:
      if self.banana.rect.colliderect(wall):
        self.holes.append(self.banana.position)
        return True
    
    return self.banana.position[1] > self.screen.get_height()
  
  def draw(self):
    self.screen.fill((245,245,245))
    
    for i, wall in enumerate(self.wall_rects):
      pygame.draw.rect(self.screen, Game.wall_colors[i % 2], wall)
    
    for hole in self.holes:
      pygame.draw.circle(self.screen, (245, 245, 245, 0), (hole[0], hole[1]), EXPLOSION_RADIUS)
    
    for player in self.players:
      player.draw(self.screen)
    
    p = self.players[self.active_player]

    pygame.draw.line(self.screen, p.color, p.position,
                     (p.position[0]+ math.cos(p.angle) * p.power,
                      p.position[1]+ math.sin(p.angle) * p.power)
                    )
    
    if self.explosion.timer > 0:
      self.explosion.draw(self.screen)

    if self.banana.visible:
      self.banana.draw(self.screen)

class Reset:
  def __init__(self, screen, chennel, font):
    self.screen = screen
    self.channel = chennel

    self.click = False
    self.menu = False

    play_again = Button(font.render("Play Again", True, "black"),
                        (260, 240),
                        self.on_hover,
                        self.on_exit,
                        self.play_again)
    
    main_menu = Button(font.render("Main Menu", True, "black"),
                       (255, 300),
                       self.on_hover,
                       self.on_exit,
                       self.return_to_menu)
    
    self.buttons = [play_again, main_menu]

    player_1_wins = font.render("Player 1 wins!", True, (60, 77, 138))
    player_2_wins = font.render("Player 2 wins!", True, (145, 45, 50))
    self.win_text = [player_1_wins, player_2_wins]
    self.winner = 0

  def play_again(self):
    self.click = True
    self.channel.play(Button.ding_sound)
    self.on_exit()

  def return_to_menu(self):
    self.menu = True
    self.channel.play(Button.ding_sound)

  def on_hover(self):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    self.channel.play(Button.tick_sound)

  def on_exit(self):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

  def update(self, dt):
    for button in self.buttons:
      button.update()
  
  def draw(self):
    self.screen.fill((245,245,245))
    self.screen.blit(self.win_text[self.winner], 
                    (self.screen.get_width()/2 - self.win_text[self.winner].get_width()/2, 200))
    
    for button in self.buttons:
      button.draw(self.screen)
