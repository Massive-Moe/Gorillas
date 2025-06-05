#THIS PROJECT FILE IS ONLY FOR THE FEW STUDENTS WHO ARE PLANNING ON USING GRAPHICS IN THEIR CULMINATING. ALL OTHER STUDENTS SHOUDL BE USING THE "CULIMINATING CODE" TEXT BASED FILE 

import pygame
from pygame.locals import QUIT
import random
import math

#Some constants
DIS_WIDTH, DIS_HEIGHT = 640, 480
BALL_SPEED = 25
GRAVITY = 2
EXPLOSION_RADIUS = 20

pygame.init()
pygame.font.init()
DISPLAYSURF = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Gorillas')
clock = pygame.time.Clock()

font = pygame.font.SysFont('dejavusans', 30)
win_text = font.render("0",0,(0,0,0))
play_again_text = font.render("Click to play again",0,(0,0,0))
gorilla_blue = pygame.image.load('gorilla_blue.png')
gorilla_blue = pygame.transform.scale(gorilla_blue, (45,45))
gorilla_red = pygame.image.load('gorilla_red.png')
gorilla_red = pygame.transform.scale(gorilla_red, (45,45))

#Compares the two circles to detect intersection
def circleCollision(circle1pos, circle2pos, circle1radius, circle2radius):
  radiusSum = circle1radius + circle2radius
  squaredX = (circle2pos[0] - circle1pos[0]) ** 2
  squaredY = (circle2pos[1] - circle1pos[1]) ** 2
  distance = squaredX + squaredY
  return (distance <= radiusSum**2)

class Player:
  angle = 0
  power = 0
  def __init__(self, position, img):
    self.position = position
    self.img = img
  def draw(self):
    DISPLAYSURF.blit(self.img, (self.position[0] - 23, self.position[1] - 35))

class Ball:
  velocity = 0
  visible = False
  rect = pygame.Rect(0,0,0,0)
  rotation = 0
  def __init__(self, color, position, radius):
    self.color = color
    self.position = position
    self.radius = radius
    self.rect.width = (radius * 2) - 6
    self.rect.height = self.rect.width
    self.banana = pygame.image.load('banana.png')
    self.banana = pygame.transform.scale(self.banana, (30,30))
    self.banana_copy = self.banana.copy()

class Explosion:
  timer = 0
  position = (0,0)

bally = Ball((255, 161, 0), (0,0), 15)
explosion = Explosion
player_colors = [(60, 77, 138),(145, 45, 50)]
wallwidth = []
wallRects = []
players = []
holes = []
turn = False

#Reset the game and setup the walls
def init_game():
  wallwidth.clear()
  for i in range(6):
    wallwidth.append(60)
  for i in range(2):
    wallwidth.append(80)
  for i in range(3):
    wallwidth.append(40)
  random.shuffle(wallwidth)
  
  wallRects.clear()
  x = 0
  for width in wallwidth:
    wallRects.append(pygame.Rect(x,
                                 random.randint(100,400),
                                 width,
                                 DIS_HEIGHT))
    x += width
  
  player1 = Player((wallRects[0].width/2, wallRects[0].y-10), gorilla_blue)
  player2 = Player((DIS_WIDTH - wallRects[-1].width/2,wallRects[-1].y-10), gorilla_red)

  global players
  #This list doesn't work without adding global for some reason
  players = [player1, player2]
  global turn
  #And this too
  turn = False
  
  holes.clear()

def playerTurn(player):
  mouseX, mouseY = pygame.mouse.get_pos()
  delta = (mouseY - player.position[1], mouseX - player.position[0])
  player.angle = math.atan2(delta[0], delta[1])
  player.power = math.sqrt(delta[0]*delta[0] + delta[1]*delta[1])
  if player.power > 50:
    player.power = 50

  if event.type == pygame.MOUSEBUTTONDOWN:
    if bally.visible == False:
      bally.visible = True
      bally.velocity = (math.cos(player.angle) * player.power, 
                        math.sin(player.angle) * player.power)
      bally.position = player.position

def updateBall(dt):
  if bally.visible:
    #Apply gravity to the ball
    bally.position = (bally.position[0] + bally.velocity[0]*dt*BALL_SPEED, 
                      bally.position[1] + bally.velocity[1]*dt*BALL_SPEED)
    bally.velocity = (bally.velocity[0],  bally.velocity[1]+dt*BALL_SPEED*GRAVITY)

    if circleCollision(bally.position, players[0].position, bally.radius, 10):
      return 3

    if circleCollision(bally.position, players[1].position, bally.radius, 10):
      return 2
    
    if bally.position[1] > DIS_HEIGHT:
      return 1

    for wall in wallRects:
      if bally.rect.colliderect(wall):
        holes.append((bally.position[0], bally.position[1]))
        return 1

    #Ignore collision if inside hole
    for hole in holes:
      if circleCollision(bally.position, hole, bally.radius, EXPLOSION_RADIUS - bally.radius):
        return 0
        
  #Must use a clean copy of the image so rotation looks correct
  bally.banana = pygame.transform.rotate(bally.banana_copy, bally.rotation)
  bally.rotation += 15
  
  if bally.rotation > 360:
    bally.rotation = 0

  bally.rect.x = bally.position[0] - bally.radius + 3
  bally.rect.y = bally.position[1] - bally.radius + 3

def update(event, dt):
  global turn
  global gameOver
  global win_text

  if not gameOver:
    playerTurn(players[turn])
  
    hit = updateBall(dt)

    explosion.timer -= dt
    
    if hit == 1:
      explosion.timer = 1
      explosion.position = (bally.position[0], bally.position[1])
      bally.visible = False
      bally.position = (0,0)
      #switches player turn
      turn = not turn
    #Make sure player doesn't hit themself
    elif hit == 3 and turn == 1:
        gameOver = True
    elif hit == 2 and turn == 0:
        gameOver = True
    win_text = font.render(f"Player {turn+1} wins!", False, player_colors[turn])
  else:
    if event.type == pygame.MOUSEBUTTONDOWN:
      init_game()
      gameOver = False
    
def draw():
  DISPLAYSURF.fill((245,245,245))
  if not gameOver:
    colors = [(200, 200, 200), (80, 80, 80)]
    for i, wall in enumerate(wallRects):
      pygame.draw.rect(DISPLAYSURF, colors[i % 2], wall)
  
    for hole in holes:
      pygame.draw.circle(DISPLAYSURF,(245,245,245, 0),(hole[0], hole[1]), EXPLOSION_RADIUS)
    
    players[0].draw()
    players[1].draw()
  
    player = players[turn]

    if explosion.timer >= 0:
      pygame.draw.circle(DISPLAYSURF, (255,0,0), explosion.position, EXPLOSION_RADIUS + explosion.timer*5)
    
    pygame.draw.line(DISPLAYSURF,player_colors[turn],player.position,
                     (player.position[0]+math.cos(player.angle) * player.power,
                      player.position[1]+math.sin(player.angle) * player.power))
    if bally.visible:
      DISPLAYSURF.blit(bally.banana, 
                       (bally.position[0] - bally.radius,
                        bally.position[1] - bally.radius))
      #pygame.draw.circle(DISPLAYSURF, (0,0,0), (bally.position[0], bally.position[1]), bally.radius, 1)
      #pygame.draw.rect(DISPLAYSURF, (0,255,0), bally.rect, 1)
  else:
    DISPLAYSURF.blit(win_text, (200, 200))
    DISPLAYSURF.blit(play_again_text, (180, 230))
  
  pygame.display.update()

init_game()

gameQuit = False
gameOver = False

while not gameQuit:
  deltaTime = clock.tick(60)/1000
  for event in pygame.event.get():
    if event.type == QUIT:
      gameQuit = True

  update(event, deltaTime)
  draw()

pygame.quit()