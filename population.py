from individual import *
import sys

class Population:

	# Create a new group of individuals that can evolve
	#
	# Generations: number of generations to produce
	# alpha: alpha value to use for line drawing color
	# bgcolor: background color to use 
	# Filename: output filename (without extension)
	# ext: file extension to use (".jpg", ".png", etc)
	# save_states: save a copy of each generation's best individual?
	def __init__(self, base_image, generations, alpha, bgcolor, filename, ext, save_states):
		self.generations = generations
		self.generation = 1
		self.alpha = alpha
		self.bgcolor = bgcolor
		self.reference = base_image
		self.filename = filename
		self.ext = ext
		self.individuals = []
		self.best_fit_individual_history = []
		self.max_fitness_history = []
		self.mean_fitness_history = []
		self.save_states = save_states

	# Initialize the genes
	# Genes are a list of lines.  Each line consists of 
	# [x1, y1, x2, y2], a set of endpoints.
	def initialize(self):
		for i in range(self.capacity):
			individual = Individual(self.base_image, self.alpha, self.bgcolor)
			self.individuals.append(individual)

	# Run all generations
	def evolve(self):
		while self.generation < self.generations:
			self.step()

	def step():
		self.generation += 1
		sys.stdout.write("STEP: " + str(self.generation) + "\n")
		sys.stdout.write("    Reproducing...")
		sys.stdout.flush()

		######### PARENTS
		parents = self.individuals

		######### MUTATIONS
		mutants = []
		# Make 50 parents asexually mutate
		for i in range(0,50):
			mutants.append(parent[i].mutate());
		# Make 25 parents asexually mutate 2 times
		for i in range(50,75):
			mutants.append(parent[i].mutate().mutate());
		# Make 25 parents asexually mutate 4 times
		for i in range(75,100):
			mutants.append(parent[i].mutate().mutate().mutate().mutate());

		######### OFFSPRING
		offspring = []
		for i in range(100):
			pair = sample(mutants, 2);
			offspring.append(pair[0].mate(pair[1]))

		######### Create merged list and sort
		sys.stdout.write("    Compute fitness...")
		sys.stdout.flush()

		pool = parents + mutants + offspring
		pool = sorted(pool, key = lambda indv: indv.fitness(self.reference), reverse=True)

		######### Prune the list down to 100 individuals:
		sys.stdout.write("    Prune individuals...")
		sys.stdout.flush()

		individuals = []
		individuals += pool[0:50] # Keep all of the 50 best fit
		individuals += sample(pool[50:150], 30) # Keep 30 of the next 100 best fit
		individuals += sample(pool[150:295], 15) # Keep 15 of the next 145 best fit
		individuals += pool[295:300] # Keep all of the 5 worst fit
		self.individuals = individuals

		######### Keep statistics
		sys.stdout.write("    Compute statistics...")
		sys.stdout.flush()

		best_fit = individuals[0]
		self.best_fit_individual_history.append(best_fit)
		self.max_fitness_history.append(best_fit.fitness(self.reference));
		self.mean_fitness_history.append(reduce(lambda acc, indv: acc + indv.fitness(self.reference), individuals, 0)/100.0)

		######### Draw historic individuals
		if self.save_states:
			sys.stdout.write("    Draw best individual of this generation...")
			sys.stdout.flush()

			best_fit.blurred().save(self.filename + "_BLUR_" + str(self.generation) + self.ext)
			best_fit.image().save(self.filename + "_NOBLUR_" + str(self.generation) + self.ext)