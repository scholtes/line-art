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
		for i in range(randint(round(self.alpha/255*self.limit), round(255/self.alpha*self.limit))):
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

	# Mate two individuals
	# Non-mutable, neither individual is modified.  A new object
	# is returned instead.
	# All offspring are also mutated right away
	def mate(self, other, base_image):
		# Create a new individual
		individual = Individual(base_image, self.alpha, self.bgcolor)

		for gene in self.genes:
			if random() < 0.5:
				# Half the time, include one parent's gene
				individual.genes.append(gene)
			# Half the time, exclude the gene

		for gene in other.genes:
			if random() < 0.5:
				# Half the time, include the other parent's gene
				individual.genes.append(gene)
			# Half the time, exclude the gene

		# Mutate and return
		return individual.mutate(base_image)



	# Mutate an individual.
	# Non-mutable process... a new object is created and returned.
	# "self" is not modified.
	# ...there are a LOT of ways this could be improved.  Lots of
	# values in here were chosen arbitrarily without any significant
	# statistical research or empirical studies done
	def mutate(self, base_image):
		# Create a new individual
		individual = Individual(base_image, self.alpha, self.bgcolor)

		#### DUPLICATE AND REMOVE GENES
		# 92% of genes are copied normally 
		# 4% of genes are copied twice
		# 4% of genes are deleted
		for gene in self.genes:
			choice = random()
			if self.in_corner(gene):
				# Don't include this gene if it's stuck in a corner
				pass
			elif choice < 0.92:
				# Just copy the gene
				individual.genes.append(gene)
			elif choice < 0.96:
				# Copy the gene twice
				individual.genes.append(gene)
				individual.genes.append(gene)
			# Else: do nothing (delete the gene)

		#### FUZZ LINE POSITIONS AND COLORS
		for i in range(len(individual.genes)):
			x1, y1, x2, y2, color = individual.genes[i]
			red, green, blue, alpha = color
			x1 = self.xfudge(x1)
			x2 = self.xfudge(x2)
			y1 = self.yfudge(y1)
			y2 = self.yfudge(y2)
			red = self.cfudge(red)
			green = self.cfudge(green)
			blue = self.cfudge(blue)
			individual.genes[i] = (x1, y1, x2, y2, (red, green, blue, alpha))

		#### ADD NEW LINES
		# Do this for 5% of individuals
		if random() < 0.05:
			for i in range(1 + round(abs(gauss(0, 50)))):
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
				individual.genes.append((x1, y1, x2, y2, color))

		#### MASS DELETE LINES
		# Do this for 5% of all individuals
		if random() < 0.05:
			individual.genes = individual.genes[1 + round(abs(gauss(0, 50))):]

		#### Shuffle order of genes
		# Matters because of how mass insertion and deletion is done.
		# It also matters because it puts selective pressure against
		# individuals whose order-of-drawing matters (not necessarily
		# desired, but time will tell)
		shuffle(individual.genes)


		#### RETURN INDIVIDUAL
		return individual

	def xfudge(self, x):
		if x == 0 or x == self.width:
			return x
		else:
			x = round(gauss(x, 0.005*self.width))
		if x < 0:
			return 0
		elif x > self.width:
			return self.width
		else:
			return x

	def yfudge(self, x):
		if x == 0 or x == self.height:
			return x
		else:
			x = round(gauss(x, 0.005*self.height))
		if x < 0:
			return 0
		elif x > self.height:
			return self.height
		else:
			return x

	def cfudge(self, x):
		x = round(gauss(x, 3))
		if x < 0:
			return 0
		elif x > 255:
			return 255
		else:
			return x

	def in_corner(self, gene):
		x1, y1, x2, y2, color = gene
		c1 = (x1==0 or x1==self.width) and (y1==0 or y1==self.height)
		c2 = (x2==0 or x2==self.width) and (y2==0 or y2==self.height)
		return c1 or c2



	# Get an Pillow.Image object for this individual.
	# We do not store this in memory because hundreds of individuals
	# need to be kept in memory at once 
	def image(self):
		raster = Image.new("RGB", (self.width, self.height), self.bgcolor)
		for line in self.genes:
			draw = ImageDraw.Draw(raster, 'RGBA')
			draw.line(line[0:4], fill = line[4])
		return raster

	# How fit is this individual?
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
		####### Slightly penalize more lines than fewer lines
		coeff = 0.95 # 1 = no penalty, 0 = max penalty
		penalty = 1.0 - (1.0 - coeff)*len(self.genes)/(self.limit)
		score = score*penalty
		####### ^^^ This penalty thing isn't working out
		self.score = score
		return score

	# Get a Pillow.Image object for this individual, but blurred.
	# This is better for computing fitness
	def blurred(self):
		radius = self.limit/max(1, len(self.genes))
		return self.image().filter(ImageFilter.GaussianBlur(radius))