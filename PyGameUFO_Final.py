import math
import pygame
import random


class Bullet:
	def __init__(self, image = 'bullet.png', x=0, y=0, angle=0, speed = 20):
		self.image = image
		
		self.x_pos = x
		self.y_pos = y
		self.angle = angle
		self.sp = speed

		self._bullet = pygame.image.load('bullet.png')
		self._bullet = pygame.transform.scale(self._bullet, (30,30))
		self._bullet = pygame.transform.rotate(self._bullet, self.angle)
		
		self.remove = False


class Meteor:
	def __init__(self, x = 0, y = 0, diameter = 20, xv = 0, yv = 0):
		
		self.image = random.randint(1,3)
		if self.image == 1:
			self.image = 'meteor.png'
		elif self.image == 2:
			self.image = 'meteor2.png'
		elif self.image == 3:
			self.image = 'meteor3.png'
		
		self.d = diameter
		
		self.x_pos = x
		self.y_pos = y
		
		self.x_vel = xv + 1
		self.y_vel = yv + 1
		
		
		self._meteor = pygame.image.load(self.image)
		self._meteor = pygame.transform.scale(self._meteor, (self.d,self.d))

		self.collided = False
		self.parent = False
		self.spawn = 0
		
		if self.d > 50:
			self.parent = True
			self.spawn = 3
		
class Velocity:
	def __init__(self, sp = 0, a = 0):
		self.angle = a
		self.sp = sp		
		self.x = sp*math.cos(self.angle*(math.pi/180))
		self.y = sp*math.sin(self.angle*(math.pi/180))

def accelerate(result):
	if result.sp > 0:
		result.sp += 0.1
	if result.sp < 0:
		result.sp -= 0.1
	return result
	
def decel(Velocities,velsum):
	velsum.x = 0
	velsum.y = 0
	for velocity in Velocities:
		if velocity.sp > 0:
			velocity.sp -= 0.1
		if velocity.sp < 0:
			velocity.sp += 0.1
		if velocity.sp > -0.1 and velocity.sp < 0.1:
			Velocities.remove(velocity)
	
	
	for x in range(len(Velocities)):
		velsum.x += Velocities[x].sp*math.cos(Velocities[x].angle*(math.pi/180))
	
		#print '===================================='
		#print 'velsum.x:', velsum.x
		velsum.y += Velocities[x].sp*math.sin(Velocities[x].angle*(math.pi/180))
		#print 'velsum.y:', velsum.y
		#print '===================================='
	
	#print len(Velocities)
	
def meteor_collision(Meteors):
	for meteor1 in Meteors:
		for meteor2 in Meteors:
			if meteor1 == meteor2:
				continue
			else:
				if ((meteor2.x_pos +(meteor2.d/2)) - (meteor1.x_pos + (meteor1.d/2)))**2 + ((meteor2.y_pos + (meteor2.d/2)) - (meteor1.y_pos + (meteor1.d/2)))**2 < ((meteor1.d/2) + (meteor2.d/2))**2:
					if meteor1.parent == True and meteor2.parent == True:
						meteor1.x_vel = meteor1.x_vel * -1
						meteor2.x_vel = meteor2.x_vel * -1
					elif meteor1.parent == True and meteor2.parent == False:
						meteor2.collided = True
									
	for meteor in Meteors:
		if meteor.collided == True:
			Meteors.remove(meteor)
	
def bullet_collision(Meteors, Bullets):
	for meteor in Meteors:
		for bullet in Bullets:
			if ((meteor.x_pos + (meteor.d/2)) - (bullet.x_pos + 15))**2 + ((meteor.y_pos + (meteor.d/2)) - (bullet.y_pos + 15))**2 < ((meteor.d/2) + 5)**2:
				meteor.collided = True
				bullet.remove = True
		if meteor.collided == True and len(Bullets) > 0:
			if meteor.parent == True:
				for num in range(meteor.spawn):
					if num == 0:
						Meteors.append(Meteor(x = meteor.x_pos, y = meteor.y_pos, diameter = int(meteor.d/3), xv = int(meteor.x_vel/3)*-1, yv = int(meteor.y_vel/3)*-1))
					elif num == 1:
						Meteors.append(Meteor(x = meteor.x_pos, y = meteor.y_pos, diameter = int(meteor.d/3), xv = int(meteor.x_vel/3), yv = int(meteor.y_vel/3)*-1))
					elif num == 2:
						Meteors.append(Meteor(x = meteor.x_pos, y = meteor.y_pos, diameter = int(meteor.d/3), xv = int(meteor.x_vel/3), yv = int(meteor.y_vel/3)))
					
			Meteors.remove(meteor)
			
	for bullet in Bullets:
		if bullet.remove == True:
				Bullets.remove(bullet)
			
def ship_collision(Meteors,alive):
	for meteor in Meteors:
		if ((meteor.x_pos + (meteor.d/2)) - x_coord)**2 + ((meteor.y_pos + (meteor.d/2)) - y_coord)**2 <= ((meteor.d/2) + 30)**2:
			alive = False
			break
	return alive
	
def spawn_meteors(Meteors,Meteor_count):
	for x in range(Meteor_count):
		Meteors.append(Meteor(x = random.randint(100,dw - 100), y = random.randint(100,dh - 100), diameter = random.randint(20,100), xv = random.randint(-6,5), yv = random.randint(-6,5)))


black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

pygame.init()

I=pygame.display.Info()
dw = int(I.current_w/2)
dh = int(I.current_h/2)
screen = pygame.display.set_mode((dw,dh))


ufo = pygame.image.load("ship.png")
ufo = pygame.transform.scale(ufo, (80,80))
ufo = pygame.transform.rotate(ufo,-90)
ufo2 = ufo

bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (dw,dh))

pygame.display.set_caption("My Game")


done = False
accel = False
alive = True
infinite = False

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

x_coord = 100
y_coord = 100

sp = 0
angle = 0
delta = 0

result = Velocity()
velsum = Velocity()

Meteor_count = 3

Velocities = []
Bullets = []
Meteors = []

spawn_meteors(Meteors,Meteor_count)

pew = pygame.mixer.Sound("pew.wav")

while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			break
		#positive y is down, negative y is up, y axis is flipped

		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				delta = 3
			if event.key == pygame.K_RIGHT:
				delta = -3
			if event.key == pygame.K_UP:
				result = Velocity(sp = 0.1, a = angle)
				accel = True
			if event.key == pygame.K_DOWN:
				result = Velocity(sp = -0.1, a = angle)
				accel = True
				
		if event.type == pygame.KEYUP:
			
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				delta = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				Velocities.append(Velocity(sp = result.sp, a = angle))
				result = Velocity(sp = 0)
				accel = False
			if event.key == pygame.K_SPACE:
				Bullets.append(Bullet(x = x_coord, y = y_coord, angle = angle, speed = 20 + result.sp))
				pew.play()
				#print len(Bullets)	
				
				
	#ALL EVENT PROCESSING GOES ABOVE

	#ALL GAME LOGIC GOES BELOW			
						
	sw = screen.get_width()
	sh = screen.get_height()
	
	if accel == True:
		result = accelerate(result)
	
	decel(Velocities,velsum)
	
	x_coord += (result.sp*math.cos(angle*(math.pi/180)) + velsum.x)
	y_coord -= (result.sp*math.sin(angle*(math.pi/180)) + velsum.y)
				
	if x_coord < 0:
		x_coord = dw
	if x_coord > dw:
		x_coord = 0
	if y_coord < 0:
		y_coord = dh
	if y_coord > dh:
		y_coord = 0	
	
	if delta != 0:
		
		if angle > 360:
			angle = 0
		
		angle = angle+delta
		ufo2 = pygame.transform.rotate(ufo,angle)
		
	newrect = ufo2.get_rect()
	newrect.center = (x_coord,y_coord)
	
	for bullet in Bullets:
		bullet.x_pos = bullet.x_pos + bullet.sp*math.cos(bullet.angle*(math.pi/180))
		bullet.y_pos = bullet.y_pos - bullet.sp*math.sin(bullet.angle*(math.pi/180))
		
		if bullet.x_pos < 0-30 or bullet.x_pos > sw-30:
			bullet.remove = True
		if bullet.y_pos > sh-30 or bullet.y_pos < 0-30:
			bullet.remove = True
	
	for bullet in Bullets:
		if bullet.remove == True:
			Bullets.remove(bullet)
	
	for meteor in Meteors:
		meteor.x_pos += meteor.x_vel
		meteor.y_pos += meteor.y_vel
	
		if meteor.x_pos < 0 or meteor.x_pos > sw-meteor.d:
			meteor.x_vel = meteor.x_vel * -1
		if meteor.y_pos > sh-meteor.d or meteor.y_pos < 0:
			meteor.y_vel = meteor.y_vel * -1
	
	alive = ship_collision(Meteors,alive)
	
	if len(Meteors) == 0:
		Meteor_count += 1
		spawn_meteors(Meteors,Meteor_count)
		x_coord = 25
		y_coord = 25
	
	elif len(Meteors) > 1:
		meteor_collision(Meteors)
		
	if len(Bullets) > 0:
		bullet_collision(Meteors, Bullets)
	
	
	#ALL GAME LOGIC GOES ABOVE
	
	#ALL CODE TO DRAW GOES BELOW
	
	screen.fill(black)
	#screen.blit(bg, (0,0))
	
	if alive == True or infinite == True:
		screen.blit(ufo2,newrect)
	
	for bullet in Bullets:
		screen.blit(bullet._bullet, (bullet.x_pos, bullet.y_pos))
	
	for meteor in Meteors:
		screen.blit(meteor._meteor, (meteor.x_pos, meteor.y_pos))
	
	pygame.display.update()
	
	clock.tick(60)
	
pygame.quit()
