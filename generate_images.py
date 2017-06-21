from individual import *
from population import *
from PIL import Image, ImageDraw, ImageChops, ImageStat

base = Image.open('samples\\circle.png')

#example = Individual(base, 64, (255, 255, 255))
#example.initialize()
##example.blurred().save('samples\\output.png')
#print(example.fitness(base))

try:
	population = Population(base, 100000, 64, (255, 255, 255), "output\\half-dome", ".jpg", True)
	population.evolve()
except KeyboardInterrupt:
	pass


print ()
print ()
print ()

print("MAX FITNESS = ")
print(population.max_fitness_history)
print ()
print ()
print("MEAN FITNESS = ")
print(population.mean_fitness_history)
print ()
print ()
print("NUM OF GENES = ")
print(population.num_of_genes_history)
print ()
print ()
print("BEST_INDIV = ")
print(population.individuals[0].genes)