"""
This is the classic flaapy bird game made with Python and Pygame.

"""
import pygame
import neat
import os
import random
pygame.font.init()


WIN_WIDHT = 400
WIN_HEIGHT = 700



BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird2.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird3.png")))]
PIPE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "pipe.png")))
BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "base.png")))	
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bg.png")))


STAT_FONT = pygame.font.SysFont("comicsans", 50)
pipes = []


class Bird():
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0 
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]		


	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):
		self.tick_count += 1

		d = self.vel*self.tick_count + 1.5*self.tick_count**2

		if d>= 16:
			d = 16


		if d < 0:
			d -= 2

		self.y += d

		if d < 0 or self.y < self.height + 50 :
			if self.tilt < self.MAX_ROTATION :
				self.tilt = self.MAX_ROTATION

		else :

			if self.tilt > -90 :
				self.tilt -= self.ROT_VEL


	def draw(self , win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME :
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = self.ANIMATION_TIME*2

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2


		rotated_image = pygame.transform.rotate(self.img , self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect( topleft = (self.x , self.y )).center )

		win.blit(rotated_image , new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class PIPE():
	GAP = 200 
	VEL = 5	

	def __init__(self, x):
		self.x = x
		self.height = 0

		self.passed = False


		self.top = 0
		self.bottom = 0 
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS , False , True)
		self.PIPE_BOTTOM = PIPE_IMGS
		

		self.set_height()


	def set_height(self):
		self.height = random.randrange(50 , 250 )
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL


	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x , self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird):
		bird_mask = bird.get_mask()
		pipe_top = pygame.mask.from_surface(self.PIPE_TOP)
		pipe_bottom = pygame.mask.from_surface(self.PIPE_BOTTOM)

		

		top_offset = (self.x - bird.x , self.top - round(bird.y))
		bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

		b_point = bird_mask.overlap(pipe_bottom, bottom_offset)
		t_point = bird_mask.overlap(pipe_top, top_offset)

		if b_point or t_point:
			return True

		return False



class Base():
	VEL = 5
	WIDTH = BASE_IMGS.get_width()
	IMG = BASE_IMGS

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0 :
			self.x1 = self.x2 +self.WIDTH
 
		if self.x2 + self.WIDTH < 0 :
			self.x2  = self.x1 +self.WIDTH



	def draw(self, win):
		win.blit(self.IMG , (self.x1, self.y))
		win.blit(self.IMG , (self.x2, self.y))




		

def draw_window(win, birds , pipes, base):
	win.blit(BG_IMGS , (0,0))
	for pipe in pipes:
		pipe.draw(win)

	# text = STAT_FONT.render("Score: " + str(score) ,1, (255,255,255))
	# win.blit(text, (WIN_WIDHT - 10 - text.get_width(), 5))
	base.draw(win)
	for bird in birds:
		bird.draw(win)
	pygame.display.update()






def main(genome, config):
	nets = []
	ge = []
	birds = []

	for _, g in genome:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(100,300))
		g.fitness = 0
		ge.append(g)


	base = Base(600)
	pipes = [PIPE(600)]
	score = 0
	win = pygame.display.set_mode((WIN_WIDHT , WIN_HEIGHT))
	clock = pygame.time.Clock()
	run = True


	
	while run:
		clock.tick(30)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False	
				pygame.quit()
				quit()
		
		pipe_ind = 0
		if len(birds) > 0:
			if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1

		else :
			run = False
			break


		for x, bird in enumerate(birds):
			bird.move()
			ge[x].fitness += 0.1
			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))
			if output[0] > 0.5 :
				bird.jump()


		base.move()
		add_pipe = False
		rem = []
		for pipe in pipes :
			for x , bird in enumerate(birds) :
				
				if pipe.collide(bird):
					ge[x].fitness -= 1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)

				

				if not pipe.passed and pipe.x < bird.y :
					pipe.passed = True
					add_pipe = True

			if pipe.x + pipe.PIPE_TOP.get_width() < 0 :
					rem.append(pipe)

			pipe.move()

		if add_pipe:
			# score += 1
			for g in ge :
				g.fitness += 5

			pipes.append(PIPE(600))

		for x, bird in enumerate(birds) :
			if bird.y + bird.img.get_height() >= 630 or bird.y < 0 :
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)

		for r in rem :
			pipes.remove(r)	



		draw_window(win,birds, pipes, base)	



	



def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
		neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run( main,50)



if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config = os.path.join(local_dir, "configuration.txt")
	run(config)
