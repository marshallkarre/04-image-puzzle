import sys, pygame, random

assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

pygame.init()

#easy to divide by four
size = (width,height) = (800,800)
dimensions = (rows,columns) = (4,4)


class Square:
	color = ''
	label = ''
	position = (-1,-1)
	dim = (0,0)
	height = 0
	visible = True
	
	def __init__(self, x, y, w, h):
		self.position = (x,y)
		self.dim = (w,h)
	
	def check_proximity(self, xy):
		''' take a x/y position (as a tuple) and see if it is next to the current position '''
		if self.position == (-1,-1): return False
		if self.position == xy: return False
		if (abs(xy[0] - self.position[0]) <= 1 and xy[1] == self.position[1]) or (abs(xy[1] - self.position[1]) <= 1 and xy[0] == self.position[0]):
			return True
		return False
	
	def swap_position(self, xy):
		''' move to new x/y (tuple) position '''
		self.position = xy
	
	def in_correct_position(self, pos):
		''' check if self.position lines up with which square this is in the list '''
		return False
	
	def draw_square(self, draw, screen):
		''' add the square to the draw object '''
		if self.visible:
			(x1,y1) = self.position
			(w,h) = self.dim
			(x,y) = (x1 * w,y1 * h)
			draw.rect(screen, self.color, (x,y,w,h))
			f = font.render(self.label,True,(0,0,0))
			(fwidth,fheight) = font.size(self.label)
			#center the font
			(fx,fy) = (x + (w - fwidth)/2,y + (h - fheight)/2)
			screen.blit(f,(fx,fy))
		return draw


def draw_puzzle(puzzle):
	screen.fill((0,0,0))
	for i in range(len(puzzle)):
		puzzle[i].draw_square(pygame.draw,screen)
	pygame.display.flip()

def calculate_xy(pos,puzzle):
	''' calculates which square is the target '''
	w = width / columns
	h = height / rows
	to_return = (int(pos[0]//w),int(pos[1]//h))
	return to_return

def randomize_puzzle(count,puzzle):
	for e in puzzle:
		if not e.visible:
			for c in range(count):
				xy = (x,y) = (e.position[0]+random.randint(-1,1),e.position[1]+random.randint(-1,1))
				if (x >= 0 and x < columns) and (y >= 0 and y < rows):
					if e.check_proximity(xy):
						for p in puzzle:
							if p.position == xy:
								p.swap_position(e.position)
								e.swap_position(xy)
	return puzzle		

#colors taken from https://yeun.github.io/open-color/
colors = [(134,142,150),(250,82,82),(230,73,128),(190,75,219),(121,80,242),(76,110,245),(34,138,230),(21,170,191),(18,184,134),(64,192,87),(130,201,30),(250,176,5),(253,126,20),(233,236,239),(255,236,153),(163,218,255)]	
#build puzzle
puzzle = []
count = 0
for j in range(columns):
	for i in range(rows):
		temp = Square(i, j, width / columns, height / rows)
		temp.color = colors[count % len(colors)]
		count = count + 1
		temp.label = str(count)
		puzzle.append(temp)
puzzle[len(puzzle)-1].visible = False

puzzle = randomize_puzzle(500,puzzle)

font = pygame.font.SysFont("arial",64)
#initialize the window
screen = pygame.display.set_mode(size)

moves = 0
draw_puzzle(puzzle)
winning = False
while not winning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		# handle MOUSEBUTTONUP
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			xy = calculate_xy(pos,puzzle)
			print(xy)
			for e in puzzle:
				if not e.visible:
					if e.check_proximity(xy):
						for c in puzzle:
							if c.position == xy:
								c.swap_position(e.position)
								e.swap_position(xy)
								draw_puzzle(puzzle)
								moves = moves + 1
			winning = True
			for i in range(len(puzzle)):
				xy = (x,y) = (i % columns, i // rows)
				if puzzle[i].position != xy:
					winning = False
			if winning:
				for e in puzzle:
					e.visible = True
print('You won in only ' + str(moves) + ' moves! Good job!')
