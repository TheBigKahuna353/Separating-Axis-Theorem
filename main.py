import pygame
from pygame.locals import *
from pygame import Vector2

pygame.init()

screen = pygame.display.set_mode((500,500))

#check if 2 lines are intersecting
def LineIntersect(line1, line2):
    #the math is from wikipedia
    x1 = line1[0].x
    y1 = line1[0].y
    x2 = line1[1].x
    y2 = line1[1].y

    x3 = line2[0].x
    y3 = line2[0].y
    x4 = line2[1].x
    y4 = line2[1].y

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return 
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den

    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if t > 0 and t < 1 and u > 0 and u < 1:
        pt = Vector2()
        pt.x = x1 + t * (x2 - x1)
        pt.y = y1 + t * (y2 - y1)
        return pt
    return



#class for sqaure
class square:
    def __init__(self,x,y,w):
        self.x = x
        self.y = y
        self.w = w
        self.centerx = self.x + w//2
        self.centery = self.y + w//2
        self.col = (255,0,0)
        self.rotation_angle = 0

    def Draw(self, outline = False):
        if outline:
            self.Outline()
        else:
            pygame.draw.rect(screen,self.col,(self.x,self.y,self.w,self.w))

    #this used the normal coordinate of an unrotated square to find new coordinates of rotated sqaure
    def GetCorner(self,tempX,tempY):
        angle = math.radians(self.rotation_angle)
        rotatedX = tempX*math.cos(angle) - tempY*math.sin(angle);
        rotatedY = tempX*math.sin(angle) + tempY*math.cos(angle);   

        x = rotatedX + self.centerx;
        y = rotatedY + self.centery;        

        return Vector2(x,y)      

    def Outline(self):
        for point1, point2 in self.Lines():
            pygame.draw.line(screen,sqr2.col,point1,point2,1)         

    #new lines method, only changed to GetCorner()
    def Lines(self):
        lines = []
        top_left = self.GetCorner(self.x - self.centerx, self.y - self.centery)
        top_right = self.GetCorner(self.x + self.w - self.centerx, self.y - self.centery)
        bottom_left = self.GetCorner(self.x - self.centerx, self.y + self.w - self.centery)
        bottom_right = self.GetCorner(self.x + self.w - self.centerx, self.y + self.w - self.centery)

        lines.append((top_left,top_right))
        lines.append((top_left,bottom_left))
        lines.append((bottom_right,top_right))
        lines.append((bottom_right,bottom_left))
        return lines

    #chnaged to this as rotation rotates around center, so need to update both x and centerx
    def Move(self,x =None, y = None):
        if x:
            self.x += x
            self.centerx += x
        if y:
            self.y += y
            self.centery += y

    #get the lines that make up the square, the outline/perameter
    #def Lines(self):
        #lines = []
        #lines.append((Vector2(self.x,self.y),Vector2(self.x+self.w,self.y)))
        #lines.append((Vector2(self.x,self.y),Vector2(self.x,self.y + self.w)))
        #lines.append((Vector2(self.x + self.w,self.y + self.w),Vector2(self.x+self.w,self.y)))
        #lines.append((Vector2(self.x + self.w,self.y + self.w),Vector2(self.x,self.y + self.w)))
        #return lines 


#draw a line inbetween the 2 squares
def DrawLineInBetween():
    #draw a line between the 2 squares, get gradient
    #to avoid divide by zero
    if abs(sqr1.x - sqr2.x) == 0:
        gradient = "infinity"
    else:
        #rise over run
        #left - right = run
        left = sqr1 if sqr1.x < sqr2.x else sqr2
        right = sqr1 if left == sqr2 else sqr2
        gradient = ((left.y - right.y)/abs(sqr1.x - sqr2.x))
    #print("gradient:",gradient)

    #get the middle point between the centers of the squares
    middle = (max(sqr1.x + sqr1.w//2, sqr2.x + sqr2.w//2) - abs(sqr1.x - sqr2.x)//2,
              max(sqr1.y + sqr1.w//2, sqr2.y + sqr2.w//2) - abs(sqr1.y - sqr2.y)//2)
    #to avoid divide by 0
    if gradient == 0:
        point1 = Vector2(middle[0], middle[1] + 100)
        point2 = Vector2(middle[0], middle[1] - 100)
    elif gradient == "infinity":
        point1 = Vector2(middle[0] - 100, middle[1])
        point2 = Vector2(middle[0] + 100, middle[1])        
    else:
        #get normal of line
        gradient = -1/gradient
        #print("normal:",gradient)

        point1 = Vector2(middle[0] + 100, middle[1] + int(-100 * gradient))
        point2 = Vector2(middle[0] - 100, middle[1] + int(100 * gradient))
        #print(point1)
        #print(point2)
        #print(middle)

    pygame.draw.line(screen,(0,255,0),point1,point2,1)

    line = (point1, point2)
    return line


sqr1 = square(100,100,50)
sqr2 = square(200,100,50)

Clock = pygame.time.Clock()

running = True
key = ""

while running:
    screen.fill((0,0,0))

    sqr1.Draw(outline=True)
    sqr2.Draw()
    line = DrawLineInBetween()

    for sqr_line in sqr1.Lines():
        pt = LineIntersect(line,sqr_line)
        if pt:
            pygame.draw.circle(screen,(0,255,255),(int(pt.x),int(pt.y)),5)

    if key == "s":
        sqr1.y += 1
    elif key == "w":
        sqr1.y -= 1
    if key == "d":
        sqr1.x += 1
    if key == "a":
        sqr1.x -= 1

    pygame.display.update()
    Clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            running = False
        if e.type == MOUSEBUTTONDOWN:
            print(e.pos)
        if e.type == KEYDOWN:
            key = e.unicode
        if e.type == KEYUP:
            key = ""
