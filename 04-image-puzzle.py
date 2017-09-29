import sys, pygame, random

assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

''' pygame stuff '''
#let pygame set itself up
pygame.init()

#window dimensions easy to divide by four
size = (width,height) = (800,800)
#puzzle dimensions
dimensions = (rows,columns) = (4,4)

font = pygame.font.SysFont("arial",64)
#initialize the window
screen = pygame.display.set_mode(size)


''' Square object '''
class Square:
	color = ''
	label = ''
	position = (-1,-1)
	size = (0,0)
	visible = True

	def __init__(self, x, y, width, height):
		self.position = (x,y)
		self.size = (width,height)

	def check_proximity(self, xy):
		''' take a x/y position (as a tuple) and see if it is next to the current position '''
		return True

	def swap_position(self, xy):
		''' move to new x/y (tuple) position '''
		self.position=xy
	def in_correct_position(self, pos):
		''' check if self.position lines up with which square this is in the list '''
		return False

	def draw_square(self, draw, screen):
		''' add the square to the draw object '''
		if self.visible:
			(x1,y1) = self.position
			(w,h) = self.size
			(x,y) = (x1 * w,y1 * h)
			draw.rect(screen, self.color, (x,y,w,h))
			f = font.render(self.label,True,(0,0,0))
			(fwidth,fheight) = font.size(self.label)
			#center the font
			(fx,fy) = (x + (w - fwidth)/2,y + (h - fheight)/2)
			screen.blit(f,(fx,fy))
		return draw


''' Other helper functions '''
def calculate_xy(pos,puzzle):
	''' calculates which square is the target '''
	(w,h) = (width / columns, height / rows)
	#the magic of integer division: we can figure out which square a mouse click happens in
	return (int(pos[0]//w),int(pos[1]//h))

def randomize_puzzle(count,puzzle):
	''' mix up the puzzle, so it can be played; count represents how much we mix it '''
	return puzzle

def draw_puzzle(puzzle):
	''' draw the puzzle on the screen '''
	for square in puzzle:
		square.draw_square(pygame.draw, screen)
	pygame.display.flip()

''' Main code body '''
#colors are in RGB format (0–255 for each value represents the intensity of the mixture of red, green, and blue, respectively)
#If you need pretty colors, I like the library at https://yeun.github.io/open-color/
colors = [(100,50,150),(250,82,82),(200,70,120),(190,75,219),(121,80,242),(70,210,200),(34,138,230),(250,200,191),(18,184,134),(64,192,87),(130,201,30),(250,176,5),(253,126,20),(200,106,239),(255,106,153),(163,218,100)]

#build puzzle
puzzle = []
count = 0
#instantiate an object. It is initialized with a x/y which-square position and a width/height (in pixels)
for j in range(columns):
	for i in range(rows):
		temp = Square(i, j, width / columns, height / rows)
		temp.color = colors[count % len(colors)]
		count = count + 1
		temp.label = str(count)
		puzzle.append(temp)
puzzle[len(puzzle)-1].visible = False

blackblock = puzzle[len(puzzle)-1]

puzzle = randomize_puzzle(500,puzzle)

moves = 0
draw_puzzle(puzzle)

''' The Game Loop '''
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		# handle MOUSEBUTTONUP
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			xy = calculate_xy(pos,puzzle)
			for blackblock in puzzle:
					if blackblock.check_proximity(xy):
						blackblock.swap_position(xy)
						draw_puzzle(puzzle)
