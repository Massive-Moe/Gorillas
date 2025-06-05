#Compares the two circles to detect intersection
def circle_collision(circle1pos, circle2pos, circle1radius, circle2radius):
  radiusSum = circle1radius + circle2radius
  squaredX = (circle2pos[0] - circle1pos[0]) ** 2
  squaredY = (circle2pos[1] - circle1pos[1]) ** 2
  distance = squaredX + squaredY
  return (distance <= radiusSum**2)