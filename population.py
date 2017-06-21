from individual import *
from functools import reduce
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
		# Don't change this value
		self.CAPACITY = 100
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
		self.num_of_genes_history = []
		self.save_states = save_states
		self.initialize()

	# Populate the population with 100 individuals
	def initialize(self):
		for i in range(self.CAPACITY):
			individual = Individual(self.reference, self.alpha, self.bgcolor)
			individual.initialize()
			self.individuals.append(individual)

	# Run all generations
	def evolve(self):
		while self.generation < self.generations:
			self.step()

	def step(self):
		self.generation += 1
		sys.stdout.write("GENERATION: " + str(self.generation) + "\n")
		sys.stdout.write("    Reproducing..." + "\n")
		sys.stdout.flush()

		######### PARENTS
		# Mutate parents = yes
		parents = [indv.mutate(self.reference) for indv in self.individuals]
		## Mutate parents = no
		#parents = self.individuals

		######### MUTATIONS
		mutants = []
		# Make 50 parents asexually mutate
		for i in range(0,50):
			mutants.append(parents[i].mutate(self.reference));
		# Make 25 parents asexually mutate 2 times
		for i in range(50,75):
			mutants.append(parents[i].mutate(self.reference).mutate(self.reference));
		# Make 25 parents asexually mutate 4 times
		for i in range(75,100):
			mutants.append(parents[i].mutate(self.reference).mutate(self.reference).mutate(self.reference).mutate(self.reference));

		######### OFFSPRING
		offspring = []
		for i in range(100):
			pair = sample(mutants, 2);
			offspring.append(pair[0].mate(pair[1], self.reference))

		######## SPONTANEOUS
		# Create 1 brand new random individual (should be very unfit in
		# future generations)
		spontaneous = Individual(self.reference, self.alpha, self.bgcolor)
		spontaneous.initialize()

		######### Create merged list and sort
		sys.stdout.write("    Compute fitness..." + "\n")
		sys.stdout.flush()

		pool = parents + mutants + offspring + [spontaneous]
		pool = sorted(pool, key = lambda indv: indv.fitness(self.reference), reverse=True)

		######### Prune the list down to 100 individuals:
		sys.stdout.write("    Prune individuals..." + "\n")
		sys.stdout.flush()

		# The pool contains 301 individuals
		individuals = []
		individuals += pool[0:50] # Keep all of the 50 best fit
		individuals += sample(pool[50:150], 30) # Keep 30 of the next 100 best fit
		individuals += sample(pool[150:290], 15) # Keep 15 of the next 140 best fit
		individuals += sample(pool[290:301], 6) # Keep  5 of the 11 worst fit
		self.individuals = individuals

		######### Keep statistics
		sys.stdout.write("    Compute statistics..." + "\n")
		sys.stdout.flush()

		best_fit = individuals[0]
		self.best_fit_individual_history.append(best_fit)
		self.max_fitness_history.append(best_fit.fitness(self.reference));
		self.mean_fitness_history.append(reduce(lambda acc, indv: acc + indv.fitness(self.reference), individuals, 0)/100.0)
		self.num_of_genes_history.append(len(best_fit.genes))

		sys.stdout.write("    Best fitness: " + str(best_fit.fitness(self.reference)) + "\n")
		sys.stdout.flush()
		sys.stdout.write("    Best fit # genes: " + str(len(best_fit.genes)) + "\n")
		sys.stdout.flush()

		######### Draw historic individuals
		if self.save_states:
			sys.stdout.write("    Draw best individual of this generation..." + "\n")
			sys.stdout.flush()

			best_fit.blurred().save(self.filename + "_BLUR_" + str(self.generation) + self.ext)
			best_fit.image().save(self.filename + "_NOBLUR_" + str(self.generation) + self.ext)

		print()