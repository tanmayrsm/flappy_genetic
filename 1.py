import pygame ,neat ,random ,os,time
pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 700

BIRDS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird1.png"))) ,
				pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird2.png"))),
				pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs" , "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

#fonts
#STAT_FONT = pygame.font.Font("D:\\Tanmay\\flappy\\JOKERMAN.TTF", 50)
STAT_FONT = pygame.font.Font("JOKERMAN.TTF", 40)


class Bird:
	IMGS = BIRDS_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self ,x ,y):
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
		d = self.vel*self.tick_count + 1.5*self.tick_count**2		#curve dir follow kar...-10 -9 -7 0 2 3 4

		if d >= 16:
			d =16	# bottom pe aya then stay there

		if d < 0:
			d -= 2	#thoda aur upar jate reh

		self.y = self.y + d

		if d < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION	#upar jate tym ..rotate by 25 deg
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL	#niche jate tym rotate full 90 deg

	def draw(self, win):
		self.img_count += 1
		if self.img_count <= self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count <= self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0
		# so when bird is nose diving it isn't flapping
		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2
		# rotate image
		rotated_image = pygame.transform.rotate(self.img,self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x ,self.y)).center)
		win.blit(rotated_image ,new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Pipe:
	GAP = 200
	VEL = 5

	def __init__(self ,x):
		self.x = x
		self.height = 0
		#self.gap = 100

		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG ,False ,True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):
		self.height = random.randrange(50 ,450)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self ,win):
		win.blit(self.PIPE_TOP ,(self.x ,self.top))
		win.blit(self.PIPE_BOTTOM, (self.x ,self.bottom))

	def collide(self ,bird):
		bird_mask = bird.get_mask()
		#to get exact bird pixels
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x ,self.top - round(bird.y))
		bottom_offset = (self.x - bird.x ,self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask ,bottom_offset)
		t_point = bird_mask.overlap(top_mask ,top_offset)

		if t_point or b_point:
			return True
		return False

class Base:
	VEL = 10
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self ,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

		#laugic to move base ka image
	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH	

	def draw(self ,win):
		win.blit(self.IMG ,(self.x1 ,self.y))
		win.blit(self.IMG ,(self.x2 ,self.y))	

class BG:
	VEL = 5
	WIDTH = BG_IMG.get_width()
	IMG = BG_IMG

	def __init__(self ,y):
		self.y = -200
		self.x1 = -80
		self.x2 = self.WIDTH

		#laugic to move base ka image
	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH	

	def draw(self ,win):
		win.blit(self.IMG ,(self.x1 ,self.y))
		win.blit(self.IMG ,(self.x2 ,self.y))




def draw_window(win,birds ,pipes ,base,bground ,score):
	#win.blit(BG_IMG ,(-80,-200))

	bground.draw(win)

	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render("Score: "+str(score) ,1 ,(255,255,255))

	text2 = STAT_FONT.render("Birds:"+str(len(birds)) ,1 ,(255,255,255))

	win.blit(text ,(WIN_WIDTH - 10 - text.get_width() ,10))
	win.blit(text2 ,(WIN_WIDTH - 10 - text.get_width() ,50))

	base.draw(win)

	for bird in birds:
		bird.draw(win)
	pygame.display.update()

def main(genomes ,config):
	birds = []
	nets = []
	ge = []
	#(id ,genome)
	for _,g in genomes:
		#  # start with fitness level of 0
		g.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(230,350))
		ge.append(g)

	base = Base(600)
	pipes = [Pipe(600)]
	bground = BG(0)

	score = 0

	win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	clock = pygame.time.Clock()
	
	run = True
	while run:
		clock.tick(150)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()

		pipe_ind = 0

		if len(birds) > 0:
			if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1

		else:
			#no birds left
			run = False
			break

		#fitness added for every second
		for x ,bird in enumerate(birds):
			bird.move()
			ge[x].fitness += 0.1

			output = nets[x].activate((bird.y ,abs(bird.y - pipes[pipe_ind].height) ,abs(bird.y - pipes[pipe_ind].bottom)))

			#tanh h acti....-1 to +1...so 0.5 h threshold
			if output[0] > 0.5:
				bird.jump()



		#bird.move()
		add_pipe = False
		rem = []
		for pipe in pipes:
			for x ,bird in enumerate(birds):
				if pipe.collide(bird):
					#game over
					#remove the bird
					#x is posn in array re
					ge[x].fitness -= 1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)




				if not pipe.passed and pipe.x < bird.x:
					pipe.passed = True
					add_pipe = True

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			pipe.move()

		if add_pipe:
			score += 1
			for g in ge:
				g.fitness += 5

			pipes.append(Pipe(600))

		for r in rem:
			pipes.remove(r)

		for x,bird in enumerate(birds):
			if bird.y + bird.img.get_height() >= 700 or bird.y < 0:
				#print("u hit ground re")
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)
				

		bground.move()
		base.move()

		draw_window(win,birds,pipes,base,bground,score)
	

#main()



def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    #set output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    #set fitness
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)