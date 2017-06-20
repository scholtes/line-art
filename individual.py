from random import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageStat

class Individual:

	# Create a new candidate individual
	def __init__(self, base_image, alpha, bgcolor):
		self.genes = []
		self.score = None
		self.width = base_image.width
		self.height = base_image.height
		self.limit = min(self.width, self.height)
		self.alpha = alpha
		self.bgcolor = bgcolor

	# Initialize the genes
	# Genes are a list of lines.  Each line consists of 
	# (x1, y1, x2, y2, color), a set of endpoints.  'color'
	# is (r, g, b), and a constant alpha value (see above)
	def initialize(self):
		for i in range(randint(1, self.limit)):
			choice = sample([1, 2, 3, 4], 2)
			x1 = randint(1, self.width)
			y1 = randint(1, self.height)
			x2 = randint(1, self.width)
			y2 = randint(1, self.height)
			color = (randint(0, 255), randint(0, 255), randint(0, 255), self.alpha)
			if choice[0] == 1:
				y1 = 0
			if choice[0] == 2:
				x1 = self.width
			if choice[0] == 3:
				y1 = self.height
			if choice[0] == 4:
				x1 = 0
			if choice[1] == 1:
				y2 = 0
			if choice[1] == 2:
				x2 = self.width
			if choice[1] == 3:
				y2 = self.height
			if choice[1] == 4:
				x2 = 0
			self.genes.append((x1, y1, x2, y2, color))

	# Get an Pillow.Image object for this individual.
	# We do not store this in memory because hundreds of individuals
	# need to be kept in memory at once 
	def image(self):
		raster = Image.new("RGB", (self.width, self.height), self.bgcolor)
		for line in self.genes:
			draw = ImageDraw.Draw(raster, 'RGBA')
			draw.line(line[0:4], fill = line[4])
		return raster

	def fitness(self, base_image):
		# First check if fitness has already been computed
		if self.score is not None:
			return self.score
		# Otherwise, if no memo, compute
		if len(self.genes) > (255/self.alpha)*self.limit: 
			return 0.0 # too many lines is penalized
		diffimg = ImageChops.difference(base_image, self.blurred())
		diff = diffimg.load()
		'''
		score = 0.0
		for x in range(self.width):
			for y in range(self.height):
				score += sum(diff[x,y])
		'''
		score = sum(ImageStat.Stat(diffimg).mean)
		'''score = 1 - score/(self.width*self.height*255*3.0)'''
		score = 1 - score/(255*3.0)
		# Slightly penalize more lines than fewer lines
		coeff = 0.9 # 1 = no penalty, 0 = max penalty
		penalty = 1.0 - (1.0 - coeff)*len(self.genes)/(self.limit)
		score = score*penalty
		self.score = score
		return score

	def blurred(self):
		radius = self.limit/max(1, len(self.genes))
		return self.image().filter(ImageFilter.GaussianBlur(radius))