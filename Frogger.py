import pygame, sys, time, random, math
pygame.init()

globalX, globalY = 0, 0
level = 1


class Screen:
	def __init__(self, width, height, caption):
		self.width = width
		self.height = height
		self.DISPLAY = pygame.display.set_mode((self.width,self.height),0,32)
		pygame.display.set_caption(caption)	 
screen = Screen(640, 640, "Frogger")



class Frog():
	width, height = 64, 64
	lifes = 3
	position = x, y = (screen.width/2)-(width/2), screen.height-height
	sens = 10
	moving = "0"
	def draw(self):
		#stop moving off screen
		if self.x+self.width > screen.width:
			self.x += screen.width-(self.x+self.width)
		elif self.x < 0:
			self.x += self.sens
			
		pygame.draw.rect(screen.DISPLAY, blue, (self.x,self.y,self.width,self.height))
		self.drawHearts()
	
	def drawHearts(self):
		y = 15
		screen.DISPLAY.blit(heartEmptyText, (20, y))
		screen.DISPLAY.blit(heartEmptyText, (60, y))
		screen.DISPLAY.blit(heartEmptyText, (100, y))
	
		if self.lifes > 0: screen.DISPLAY.blit(heartText, (20, y))
		if self.lifes > 1: screen.DISPLAY.blit(heartText, (60, y))
		if self.lifes > 2: screen.DISPLAY.blit(heartText, (100, y))

	def move(self, forward=True):
		if self.moving == "right":
			self.x += self.sens
		elif self.moving == "left":
			self.x -= self.sens
		elif forward:
			self.y -= 64
		else:
			self.y += 64
		
		if self.y == 0:
			global level
			level += 1
			self.x = (screen.width/2)-(self.width/2)
			self.y =  screen.height-self.height
		
			
	
	def hit(self):
		self.lifes -= 1
		self.x, self.y = (screen.width/2)-(self.width/2), screen.height-self.height
		global globalY
		globalY = 0
		if self.lifes == -1:
			self.gameOver()
		
		
	def gameOver(self):
		self.lifes = 3
		global level
		level = 1
		
		
frog = Frog()
	
class Track():
	width = screen.width
	height = 64
	def __init__(self, num, delay, direction):
		self.delay = delay
		self.num = num-1
		self.y = self.positionCalc(num)
		self.direction = direction
		if direction == "right":
			self.cartX1 = 0
		else:
			self.cartX1 = screen.width
	
	def positionCalc(self, pos):
		global globalY
		pos = pos * 64 
		pos = screen.height - pos
		return pos
		
	def draw(self, frameNumber, trainNumber):
		global level
		trackX = 0
		for i in range(10):
			screen.DISPLAY.blit(trackText, (trackX, self.y + globalY))
			trackX += 64
		trackX = 0
		
		#draw carts
		if self.delay < frameNumber:
			spacing = 50
			
			for i in range(2):
				self.drawCarts(self.num+level-1, self.cartX1)#number of carts
		
		
			if self.direction == "right": 
				self.cartX1 += random.randint(1, 3)+math.floor(level/2) #animation
			else:
				self.cartX1 -= random.randint(1, 3)+math.floor(level/2)
				
	def drawCarts(self, cartNumber, pos):
		global globalY
		cartX = pos
		
		for order in range(cartNumber):
			if order < 1:
				if self.direction == "right":
					screen.DISPLAY.blit(engineText, (cartX-80, self.y + globalY))
				else:
					screen.DISPLAY.blit(engineText, (cartX+80, self.y + globalY))
			else:
				if self.direction == "right":
					screen.DISPLAY.blit(cartText, (cartX-80, self.y + globalY))
				else:
					screen.DISPLAY.blit(cartText, (cartX+80, self.y + globalY))
			
			if self.direction == "right":	
				cartX -= 85
			else: cartX += 85
		
		if self.direction == "right":
			if self.cartX1-cartNumber*90 > screen.width + 100:
				self.cartX1 = 0
		else:
			if self.cartX1 + cartNumber * 90 < -200:
				self.cartX1 = screen.width
		
		#collision detection
		if self.direction == "right":
			if frog.x < self.cartX1 and frog.x+64 > self.cartX1-cartNumber * 80 -5:
					if frog.y == self.y+globalY:
						frog.hit()
		else:
			if frog.x < self.cartX1 + cartNumber * 80 + 80 and frog.x + 64 > self.cartX1 + 80:
					if frog.y == self.y:
						frog.hit()
		

def drawBackground():
	for y in range(0, 9):
		for x in range(screen.width/64):
			screen.DISPLAY.blit(grassText, (x*64, screen.height- y * 64 + globalY-64))
	for y in range(9, 10):
		for x in range(screen.width/64):
			screen.DISPLAY.blit(stoneText, (x*64, screen.height- y * 64 + globalY-64))

def drawLevel():
	label = mainFont.render("Level " + str(level), 1, (255,255,255))
	screen.DISPLAY.blit(label, (450, 13))

blue=(0,0,255)

grassText = pygame.image.load('resources/textures/grass.bmp')
stoneText = pygame.image.load('resources/textures/stone.bmp')

trackText = pygame.image.load('resources/textures/rail.bmp')
cartText =  pygame.image.load('resources/textures/minecart.bmp')
engineText = pygame.image.load('resources/textures/engine.bmp')


heartText = pygame.image.load('resources/textures/heart.bmp')
heartEmptyText = pygame.image.load('resources/textures/heartEmpty.bmp')
mainFont = pygame.font.Font('resources/fonts/Minecraft.ttf', 40)

keys=pygame.key.get_pressed()


def main():
	
	#Declarations
	track1 = Track(2, random.randint(0, 10), "right")
	track2 = Track(3, random.randint(0, 100), "left")
	track3 = Track(4, random.randint(0, 10), "right")
	track4 = Track(5, random.randint(0, 10), "left")
	track5 = Track(6, random.randint(0, 10), "right")
	track6 = Track(7, random.randint(0, 10), "left")
	track7 = Track(8, random.randint(0, 10), "right")
	track8 = Track(9, random.randint(0, 10), "right")

	
	
	frameNumber = 0
	clock = pygame.time.Clock()
	while True:
		
		#Process events
		for event in pygame.event.get():
			
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					frog.moving = "left"
				if event.key == pygame.K_RIGHT:
					frog.moving = "right"
				if event.key == pygame.K_SPACE:
					frog.move()
				if event.key == pygame.K_b:
					frog.move(False)
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					frog.moving = "0"
				if event.key == pygame.K_RIGHT:
					frog.moving = "0"
					
		if frog.moving == "left":
			frog.move()
		elif frog.moving == "right":
			frog.move()
		
				
		#start display mode
		screen.DISPLAY.fill((255, 255, 255))
		drawBackground()
		track1.draw(frameNumber, 1)
		track2.draw(frameNumber, 1)
		track3.draw(frameNumber, 1)
		track6.draw(frameNumber, 1)
		track7.draw(frameNumber, 1)
		
		
		
		if level > 3:
			track4.draw(frameNumber, 1)
		if level > 5:
			track5.draw(frameNumber, 1)
		if level > 8:
			track8.draw(frameNumber, 1)
		
		drawLevel()
		frog.draw()
		
		#end display mode
		clock.tick(50)
		pygame.display.flip()
		frameNumber += 1
main()
