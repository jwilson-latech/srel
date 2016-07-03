import pygame
import os
import numpy as np
from numpy import pi, sin, cos, sqrt, abs,dot
import math
from numpy.linalg import inv, norm
import colorsys
# it is better to have an extra variable, than an extremely long line.
def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a
        
red = (255,0,0)
yel = (255,255,0)
blue = (0,0,255)
white = (255,255,255)
    
CELERITAS = 5
SIZE = 700

propertime = 0

class Bird(object):  # represents the bird, not the game
    def __init__(self):
        self.angle = 0
        self.angle_vector = 0
        self.normal_vector = 0
        self.angular_velocity = 0
        self.position = np.array([SIZE/2,SIZE/2])
        self.velocity = np.array([0,0])
        self.acceleration = np.array([0,0])
        self.speed = sqrt(dot(self.velocity,self.velocity))
        self.time = 0.0
        self.blink=0
        self.points = self.get_points()
        self.bow = self.points[0]
        self.inttime = 0
    def gamma(self):
        return 1/sqrt(1-dot(self.velocity,self.velocity)/CELERITAS**2)
    def get_angle_vector(self):
        self.angle_vector = np.array([-cos(self.angle*pi/180.0),+sin(self.angle*pi/180.0)])
    def get_normal_vector(self):
        self.normal_vector = np.array([-sin(self.angle*pi/180.0),-cos(self.angle*pi/180.0)])
    def handle_keys(self):
        """ Handles Keys """
        global bullets
        key = pygame.key.get_pressed()
        dist = 10/self.gamma()**(1/2) # distance moved in 1 frame, try changing it to 5
        dist2= 1/self.gamma()**(1/2)
        self.get_angle_vector()
        self.get_normal_vector()
        if key[pygame.K_DOWN]: # down key
            self.acceleration = self.acceleration-dist2*self.angle_vector*self.gamma()**(-3/2) 
        elif key[pygame.K_UP]: # up key
            self.acceleration = self.acceleration+dist2*self.angle_vector*self.gamma()**(-3/2) 
        if key[pygame.K_RIGHT]: # right key
            self.angular_velocity -= dist # move up
        elif key[pygame.K_LEFT]: # left key
            self.angular_velocity += dist # move up
        if key[pygame.K_SPACE]: # left key
           self.velocity = 0.92*self.velocity # move up
           if self.speed < 10.0**(-3):
               self.velocity = np.zeros(2)
               
        if key[pygame.K_t]: # left key
            #self.velocity = 0.92*self.velocity # move up
            bullets = []
        if key[pygame.K_v]:
            self.angle = 0
        if key[pygame.K_c]:
            self.angle = self.angle+10
        self.velocity = (self.velocity + self.acceleration)/(1+norm(self.velocity)*norm(self.acceleration)/CELERITAS**2)
        self.acceleration=0
        self.angle  = self.angle + self.angular_velocity
        
    def draw(self, surface):
        key = pygame.key.get_pressed()
        """ Draw on surface """
        # blit yourself at your current position
        self.position = np.remainder(self.position+self.velocity,SIZE)
        self.speed = sqrt(dot(self.velocity,self.velocity))
        timer = int(self.time)
        if (timer%1==0):
            pygame.draw.polygon(surface,red,self.get_points())
            if (timer != self.inttime):
                self.inttime = timer
                if key[pygame.K_d]:
                    self.shoot_photon()
                if key[pygame.K_f]: # left key
                    #self.velocity = 0.92*self.velocity # move up
                    self.shoot_bullet()
        else:
            pygame.draw.polygon(surface,yel,self.get_points())
        self.get_angle_vector()
        vx = self.velocity[0]
        vy = self.velocity[1]
        #print np.array([vx/CELERITAS,vy/CELERITAS,sqrt((vx**2+vy**2))/CELERITAS])
        self.angular_velocity = 0
        time_add = 1.0*np.sqrt(1-(vx**2+vy**2)/CELERITAS**2)
        self.time+= time_add
        print time_add
        #print int(1/(self.time-self.blink))
    
    def get_points(self):
        self.get_angle_vector()
        self.get_normal_vector()
        center = self.position
        v = np.sqrt( np.dot(self.velocity,self.velocity) )
        g = np.sqrt(1-v**2/CELERITAS**2)
        
        if v==0:
            vv=np.zeros(2)
        else:
            vv = self.velocity/v
        uu =np.array([-vv[1],vv[0]])
        tang =  self.angle_vector
        norm = self.normal_vector
        off1 = 20*tang
        off2 = -25*(tang+norm)
        off3 = -10*tang
        off4 = -25*(tang-norm)
        mat = np.array([vv*g,uu])
        if self.speed > 0: 
            imat = inv(np.array([vv,uu]))
            off1 = np.dot(imat,np.dot(mat,off1))
            off2 = np.dot(imat,np.dot(mat,off2))
            off3 = np.dot(imat,np.dot(mat,off3))
            off4 = np.dot(imat,np.dot(mat,off4))
        point1 = center + off1
        point2 = center + off2
        point3 = center + off3
        point4 = center + off4
        points = [point1,point2,point3,point4]
        self.bow = off1
        return totuple(points)
    def shoot_bullet(self):
        #if self.load>=200.0:
        bullet = Bullet(self.position,self.angle_vector,self.velocity,10)
        bullets.append(bullet)
    def shoot_photon(self):
        #if self.load>=200.0:
        photon = Photon(self.position,self.angle_vector,self.velocity,self.bow)
        bullets.append(photon)
         #   self.load=0.0
        
        
        
class Photon(object):
    def __init__(self,position,angle_vector,velocity,bow):
        self.angle_vector = angle_vector
        self.position = position + bow
        self.velocity = velocity
        self.color = np.array(self.colorize())*255
        
    def update(self):
        self.position=self.position+CELERITAS*self.angle_vector
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        self.update()
        self.position = np.remainder(self.position,SIZE)
        x = int(self.position[0])
        y = int(self.position[1])
        pygame.draw.circle(surface,self.color,[x,y],1)
    def colorize(self):
        beta = self.velocity/CELERITAS
        h = 0.375+np.dot(beta,self.angle_vector)*0.375
        return colorsys.hsv_to_rgb(h,1,1)
        
        
        
class Bullet(object):
    def __init__(self,position,angle_vector,velocity,boost):
        self.angle_vector = angle_vector
        self.position = position
        self.velocity = (velocity + boost*angle_vector)/(1+norm(velocity)*boost/CELERITAS**2)
    def update(self):
        self.position = self.position +self.velocity
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        self.update()
        self.position =self.position
        x = int(self.position[0])
        y = int(self.position[1])
        pygame.draw.circle(surface,blue,[x,y],1)
        
    
bullets = []
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))

bird = Bird() # create an instance
clock = pygame.time.Clock()

running = True
while running:
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    bird.handle_keys() # handle the keys

    screen.fill((0,0,0)) # fill the screen with white
    bird.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    # draw the bird to the screen
    pygame.display.update() # update the screen

    clock.tick(100)