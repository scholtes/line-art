from individual import *
from population import *
from PIL import Image, ImageDraw, ImageChops, ImageStat

base = Image.open('samples\\half-dome.jpg')

example = Individual(base, 64, (255, 255, 255))
example.initialize()
#example.blurred().save('samples\\output.png')

print(example.fitness(base))
print(ImageStat.Stat(ImageChops.difference(base, example.blurred())).mean)