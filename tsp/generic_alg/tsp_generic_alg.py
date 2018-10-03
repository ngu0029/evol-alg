# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:56:19 2018

@author: T901
"""

'''
Created on 2009-10-29
@author: Administrator
'''
import sys, random
from math import sqrt
from pickle import *
import pandas as pd

PIL_SUPPORT = None
try:
   from PIL import Image, ImageDraw, ImageFont
   PIL_SUPPORT = True
except:
   PIL_SUPPORT = False 

def cartesian_matrix(coords):
   """ A distance matrix """
   matrix = {}
   for i, (x1, y1) in enumerate(coords):
      for j, (x2, y2) in enumerate(coords):
         dx, dy = x1 - x2, y1 - y2
         dist = sqrt(dx * dx + dy * dy)
         matrix[i, j] = dist
   return matrix 

def tour_length(matrix, tour):
   """ Returns the total length of the tour """
   total = 0
   num_cities = len(tour)
   for i in range(num_cities):
      j = (i + 1) % num_cities
      city_i = tour[i]
      city_j = tour[j]
      total += matrix[city_i, city_j]
   return total

def write_tour_to_img(coords, tour, title, img_file):
   """ The function to plot the graph """
   padding = 20
   coords = [(x + padding, y + padding) for (x, y) in coords]
   maxx, maxy = 0, 0
   for x, y in coords:
      maxx = max(x, maxx)
      maxy = max(y, maxy)
   maxx += padding
   maxy += padding
   img = Image.new("RGB", (int(maxx), int(maxy)),\
         color=(255, 255, 255))
   font = ImageFont.load_default()
   d = ImageDraw.Draw(img);
   num_cities = len(tour)
   for i in range(num_cities):
      j = (i + 1) % num_cities
      city_i = tour[i]
      city_j = tour[j]
      x1, y1 = coords[city_i]
      x2, y2 = coords[city_j]
      d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
      d.text((int(x1) + 7, int(y1) - 5), str(i), \
        font=font, fill=(32, 32, 32)) 

   for x, y in coords:
      x, y = int(x), int(y)
      d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0),\
                fill=(196, 196, 196))

   d.text((1,1),title,font=font,fill=(0,0,0))      

   del d
   img.save(img_file, "PNG")
   print("The plot was saved into the %s file." % (img_file,))

cm = []
coords = [] 

def eval_func(chromosome):
   """ The evaluation function """
   global cm
   return tour_length(cm, chromosome) 

def cities_random(cities, xmax=800, ymax=600):
   """ get random cities/positions """
   coords = []
   for i in range(cities):
      x = random.randint(0, xmax)
      y = random.randint(0, ymax)
      coords.append((float(x), float(y)))
   return coords

def read_coords(coord_file):
    '''
    read the coordinates from file and return the distance matrix.
    coords should be stored as comma separated floats, one x,y pair per line.
    '''
    coords=[]
    for line in coord_file:
        x,y=line.strip().split(',')
        coords.append((float(x),float(y)))
    return coords

#Individuals
class Individual:
    #score = 0
    #length = 30
    seperator = ' '
    def __init__(self, chromosome=None, length=100):
        self.length = length # make as first assignment
        self.chromosome = chromosome or self._makechromosome()
        #self.length = length
        self.score = 0  # set during evaluation  

    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        chromosome = []
        lst = [i for i in range(self.length)]
        for i in range(self.length):
            choice = random.choice(lst)
            lst.remove(choice)
            chromosome.append(choice)
        #shorter version: chromosome = np.random.permutation(lst)
        return chromosome

    def evaluate(self, optimum=None):
        self.score = eval_func(self.chromosome)

    def crossover(self, other):
        left, right = self._pickpivots()
        p1 = Individual()
        p2 = Individual()
        # removing (right-left+1) genes appearing in other.chromosome[left:right+1] from self.chromosome
        # note that self.chromosome and other.chromosome have the same genes but in different order
        # c1 has length of (self.length-(right-left+1))=(self.length-(right+1)+left) >= left
        c1 = [ c for c in self.chromosome \
               if c not in other.chromosome[left:right + 1]]
        # inserting (right-left+1) genes of other.chromosome[left:right+1] in c1 (part of self.chromosome)
        p1.chromosome = c1[:left] + other.chromosome[left:right + 1]\
                         + c1[left:]
        # the same thing: remove genes then insert the same genes, but their ordering in the chromosome has changed
        c2 = [ c for c in other.chromosome \
               if c not in self.chromosome[left:right + 1]]
        p2.chromosome = c2[:left] + self.chromosome[left:right + 1] \
                        + c2[left:]
        return p1, p2
    
    def reverse(self):
        p = Individual()
        c=self.chromosome[:]  # make copy, not to mutate the orignal list
        left, right = self._pickpivots()
        if random.random() < 0.5:
            c[left:right+1]=reversed(self.chromosome[left:right+1])
        else:
            c[right+1:]=reversed(self.chromosome[:left])
            c[:left]=reversed(self.chromosome[right+1:])
        p.chromosome = c
        return p

    def mutate(self):
        "swap two element"
        left, right = self._pickpivots()
        temp = self.chromosome[left]
        self.chromosome[left] = self.chromosome[right]
        self.chromosome[right] = temp
        # shorter version: self.chromosome[lelf], self.chromosome[right] = self.chromosome[right], self.chromosome[left]

    def _pickpivots(self):
        left = random.randint(0, self.length - 2)
        right = random.randint(left, self.length - 1)
        return left, right    

    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str, self.chromosome)), self.score)  

    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin

    def __cmp__(self, other):
        # https://portingguide.readthedocs.io/en/latest/comparisons.html
        # cmp() function was removed in Python 3.
        # return cmp(self.score, other.score)
        return (self.score > other.score) - (self.score < other.score)
    
    def __lt__(self, other):
        return self.score < other.score

class Environment:
    #size = 0
    def __init__(self, population=None, size=1000, maxgenerations=10,\
                 newindividualrate=0.3,crossover_rate=0.90,\
                 mutation_rate=0.005, mutate_type='whole', evol_operator='crossover'):
        self.size = size
        self.population = self._makepopulation()
        self.maxgenerations = maxgenerations
        self.newindividualrate = newindividualrate
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        for individual in self.population:
            individual.evaluate()  # score each individual by its length
        self.generation = 0
        #self.minscore = sys.maxint
        self.minscore = sys.maxsize  # https://stackoverflow.com/questions/13795758/what-is-sys-maxint-in-python-3
		#self.minindividual = None
        self.minindividual = Individual()  # create a new Individual instance instead of being assigned to one poppulation instance to AVOID MUTATED LIST ISSUE
        self.mutate_type=mutate_type
        self.evol_operator=evol_operator
        #self._printpopulation()
        if PIL_SUPPORT:
            write_tour_to_img(coords, self.population[0].chromosome, 'score = %f'%self.minscore,\
                              "TSPstart_GA_mutate_" + self.mutate_type + ".png")
        else:
            print("No PIL detected,can not plot the graph")

    def _makepopulation(self):
        return [Individual() for i in range(0, self.size)]

    def run(self):
        for i in range(1, self.maxgenerations + 1):
            if i%200 == 1: print("Generation no:" + str(i))
            # FITNESS EVALUTATION STEP 
            # check in current generation who is the best-score individual
            # for each generation, always find the best individual and record it if it is better than that of last generation
            for j in range(0, self.size):
                self.population[j].evaluate() # this is already done for the 1st generation during __init__
                curscore = self.population[j].score
                if curscore < self.minscore:
                    self.minscore = curscore
                    self.minindividual.score = self.population[j].score
					self.minindividual.chromosome = self.population[j].chromosome[:]  # should be copied since self.population[i] could be mutated in mutation step
            if i%200 == 1: print("Best individual:", self.minindividual)
            if random.random() < self.crossover_rate:
                children = []
                if self.evol_operator == 'crossover':
                    newindividual = int(self.newindividualrate * self.size / 2)  # len(children) = 2*newindividual < self.size
                    for i in range(0, newindividual):
                        selected1 = self._selectrank()
                        selected2 = self._selectrank()
                        parent1 = self.population[selected1]
                        parent2 = self.population[selected2]
                        child1, child2 = parent1.crossover(parent2)
                        child1.evaluate()
                        child2.evaluate()
                        children.append(child1)
                        children.append(child2)
                elif self.evol_operator == 'reverse':
                    newindividual = int(self.newindividualrate * self.size)  # len(children) = newindividual < self.size
                    for i in range(0, newindividual):
                        selected = self._selectrank()
                        child = self.population[selected].reverse()
                        child.evaluate()
                        children.append(child)
                #for i in range(0, newindividual):
                for i in range(0, len(children)):
                    #replace with child
                    totalscore = 0
                    for k in range(0, self.size):
                        totalscore += self.population[k].score
                    randscore = random.random() # generates a random float uniformly in the semi-open range [0.0, 1.0)
                    addscore = 0
                    for j in range(0, self.size):
                        addscore += (self.population[j].score / totalscore) # the final addscore (end loop) = 1 > randscore
                        if addscore >= randscore:
                            self.population[j] = children[i]   # do not need to copy children[i] since children[i] is a new instance, see in crossover()
                            break # IMPORTANT, replace only one parent by a child then move to next child i
            if self.mutate_type == 'whole':  # mutation is looped over the whole generation to increase the diversity
                for i in range(0, self.size):
                    if random.random() < self.mutation_rate:
                        #self.population[i].mutate()  # this might ruin the generation since better individuals are also mutated
                        selected = self._select()  # this is likely selecting worse individuals for mutation
                        self.population[selected].mutate()							
            else:
                if random.random() < self.mutation_rate:
                    selected = self._select()
                    self.population[selected].mutate() # only one individual in population is mutated for each generation
                                                       # WE PROBABLY USE MUTATE PROBABILITY FOR WHOLE GENERATION             
        #end loop
        # check in last generation who is the best-score individual
        for i in range(0, self.size):
                self.population[i].evaluate()
                curscore = self.population[i].score
                if curscore < self.minscore:
                    self.minscore = curscore
                    self.minindividual.score = self.population[i].score
					self.minindividual.chromosome = self.population[i].chromosome[:]  # should be copied since self.population[i] could be mutated in mutation step
        print("..................Result.........................")
        print(self.minindividual)
        #self._printpopulation()
        
        return self.minscore

    def _select(self):
        totalscore = 0
        for i in range(0, self.size):
            totalscore += self.population[i].score
        randscore = random.random()*(self.size - 1)
        addscore = 0
        selected = 0
        for i in range(0, self.size):
            addscore += (1 - self.population[i].score / totalscore) # the final addscore (end loop) = (self.size - 1) > randscore
            if addscore >= randscore:
                selected = i
                break
        return selected

    def _selectrank(self, choosebest=0.9):  # the higher the para choosebest is, the more probable the better parent is chosen
        self.population.sort() # ascending order, lower score means better individual
        if random.random() < choosebest: # choose better individual
            return random.randint(0, self.size * self.newindividualrate)
        else: # choose worse individual
            return random.randint(self.size * self.newindividualrate,\
                   self.size - 1) # including two ends while np.random.randint excludes the high end.

    def _printpopulation(self):
        for i in range(0, self.size):
            print("Individual ", i, self.population[i])

def main_run():
    global cm, coords
    #get cities's coords
    #coords =cities_random(30)
    coords=read_coords(open('D:/github/evol-alg/tsp/generic_alg/city100.txt'))
    cm = cartesian_matrix(coords)
    num_runs = 10
    mutate = 'whole' # 'one' or 'whole
    pop_sizes = [1000, 1000, 1000]
    maxgens = [1000, 1000, 1000]
    birthrates = [0.2, 0.3, 0.4]
    crossrates = [0.9, 0.9, 0.9]
    mutrates = [0.005, 0.005, 0.005]
    operators = ['crossover', 'reverse'] # 'crossover', 'reverse', 'swap'
    for p in range(len(birthrates)):
        for operator in operators:
            print("..................Start.........................")
            print('birthrate =', birthrates[p], 'operator =', operator)
            scores = []
            for i in range(num_runs):
                print('Run:', str(i))
                ev = Environment(size=pop_sizes[p], maxgenerations=maxgens[p],\
                                 newindividualrate=birthrates[p],crossover_rate=crossrates[p],\
                                 mutation_rate=mutrates[p], mutate_type = mutate, evol_operator = operator)
                score = ev.run()
                scores.append(score)
                if PIL_SUPPORT:
                    write_tour_to_img(coords, ev.minindividual.chromosome, 'score = %f'%score, \
                                      "TSPresult_GA_mutate_" + mutate + ".png")
                    print('')
                else:
                    print("No PIL detected,can not plot the graph")
            avg_score = sum(scores)/len(scores)
            scores_df = pd.DataFrame([range(num_runs), scores], index = ['run', 'score'])
            scores_df.to_csv('tsp_genalg_paraset_' + str(p) + '_oper_' + operator + '_score_' + '%.02f' %avg_score + '.csv', index = True)
            print("AVERAGE ON RUNS =%.02f", avg_score)
            print("..................End.........................")
            print('')
if __name__ == "__main__":
    main_run()