from individual import *

class Population:

	# Create a new group of individuals that can evolve
	#
	# Generations: number of generations to produce
	# alpha: alpha value to use for line drawing color
	# bgcolor: background color to use 
	# Filename: output filename (without extension)
	# ext: file extension to use ("jpg", "png", etc)
	# save_states: save a copy of each generation's best individual?
	def __init__(self, base_image, generations, alpha, bgcolor, filename, ext, save_states):
		self.capacity = 100
		self.generations = generations
		self.generation = 1
		self.alpha = alpha
		self.bgcolor = bgcolor
		self.reference = base_image
		self.filename = filename
		self.ext = ext
		self.individuals = []
		self.fitness_history = []
		self.save_states = save_states

	# Initialize the genes
	# Genes are a list of lines.  Each line consists of 
	# [x1, y1, x2, y2], a set of endpoints.
	def initialize(self):
		for i in range(self.capacity):
			individual = Individual(self.base_image, self.alpha, self.bgcolor)
			self.individuals.append(individual)