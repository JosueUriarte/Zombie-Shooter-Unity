import sys
import os
import copy
import heapq
import multiprocessing.pool as mpool
import os
import random
import shutil
import time
import math
from math import inf, sqrt
from heapq import heappop, heappush

width = 100
height = 84

#How many spawn points to have on a map
spawnPoints = 5
#the character "S" is a zombie spawn point

options = [
  "R", #Rock
  "-", 
  "H", 
  "V"  #Empty Space
]

class Individual_Grid(object):
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None
    
    def replaceGenome(self, genome):
        self.genome = copy.deepcopy(genome)
        
    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.
    def calculate_fitness(self):
        #this function calculates fitness based on percentage of empty space
        #add metrics for pathfinding, A*
        #UPDATE THIS FUNCTION, if their is a path from start to finish then update fitness by some measure
        totalSpace = height * width
        totalInitial = height * width
        genome = self.to_level()
        for y in range(height):
            for x in range(width):
                if genome[y][x] != "-":
                    totalSpace = totalSpace - 1   
        self._fitness = totalSpace / totalInitial
        return self
    

    # Return the cached fitness value or calculate it as needed.
    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        return self._fitness

    
    # Mutate a genome into a new genome.  Note that this is a _genome_, not an individual!
    def mutate(self, genome):
        hWallOffsetX = 10 #how much space between horizontal walls that are needed

        vWallOffsetX = 5 #how much space between vertical walls that are needed

        new_genome = copy.deepcopy(self.genome) #make a copy of the genome were working with
        
        for y in range(height):
            itemsRemoved = 50 #maximum items that can be removed per row
            
            itemsAdded = 10 #maximum items that can be added per row, resets to 3 every row

            addLimit = 0 #threshold for x value of (y, x). Specific offset for that prefab (rock, vertical wall, horizontal wall, etc) is added to threshold

            #if x is above this threshold than your allowed to place (rock, vertical wall, etc) at that point

            for x in range(width):
                if new_genome[y][x] != '-' and itemsRemoved != 0 and random.randint(1, 30) == 10: #if (y, x) on genome is not empty i.e its a prefab
                    #percent chance of this happening on a (y, x)
                    #determined by random.randint(a, b) = c ******PLAY****** around with a, b, cs for better results

                    new_genome[y][x] == '-' #replace with empty prefab

                    itemsRemoved = itemsRemoved - 1 #decrement itemsRemoved
                else:
                    if x >= addLimit and itemsAdded != 0 and y % 2 == 0 and random.randint(1, 100) == 10: #if (y, x) is empty ('-') and y is even -> place prefab
                        prefab = random.choice(options) #pick a random prefab

                        if prefab == 'H':
                            addLimit = x + hWallOffsetX #increase addLimit by the offset for vertical wall
                            new_genome[y][x] = prefab #place prefab at that spot
                                
                        if prefab == 'V':
                            addLimit = x + vWallOffsetX #increae addLimit by the offset for vertical wall
                            new_genome[y][x] = prefab #place prefab at that spot
                                
                        itemsAdded = itemsAdded - 1 #decrement itemsAdded
        
        #this function de-clutters the genome as well as adds zombie spawn points
        return genomeClear(new_genome)

    #returns two children 
    def generate_children(self, other):
        parent1 = self.genome
        parent2 = other.genome

        #added to avoid index out of bounds
        h = height - 1
        w = width - 1

        g1 = [["-" for col in range(width)] for row in range(height)] #generate the appropriate size genome
        g2 = [["-" for col in range(width)] for row in range(height)] #generate the appropriate size genome
        
        point_H1 = random.randint(0, h)
        point_W1 = random.randint(0, w)

        point_H2 = random.randint(point_H1, h)
        point_W2 = random.randint(point_W1, w)

        for y in range (0, point_H1):
            for x in range (0, point_W1):
                g1[y][x] = parent1[y][x]
                g2[y][x] = parent2[y][x]

        for y in range (point_H1, point_H2):
            for x in range (point_W1, point_W2):
                g1[y][x] = parent2[y][x]
                g2[y][x] = parent1[y][x]

        '''
        for y in range (point_H2, height + 1):
            for x in range (point_W2, width + 1):
                g1[y][x] = parent1[y][x]
                g2[y][x] = parent2[y][x]
        '''
        for y in range (point_H2, height):
            for x in range (point_W2, width):
                g1[y][x] = parent1[y][x]
                g2[y][x] = parent2[y][x]

        #The new genome which is g = [] is initialized to be empty
        #for the top half, all the genes from first parent are copied
        #for the bottom half, all the genes from the second parent are copied

        #PLAY AROUND WITH THIS, MAKE IT BETTER
                
        #returns two children, each with same genome, initially before going into mutation
        return Individual_Grid(self.mutate(g1)), Individual_Grid(self.mutate(g2))
        

    # Turn the genome into a level string (easy for this genome)
    def to_level(self):
        return self.genome


    @classmethod
    def jrod_individual(cls):
        offsetY = 10 

        offsetX = 10 
        #refer to createRoom() for details, these offsets are for when a room is generated it has the appropriate spacing
        #these offsets can be changed for different dimentions on the rooms 
        
        rooms = 7 #number of rooms to generate
        
        doNotReuse = [] #list of coordinates where you can't call createRoom()
        
        yRange = height - offsetY - 1
        xRange = width - offsetX - 1
        #we dont want the to place stuff on the coordinates at the edges, hence the offset, to prevent a horizontal wall from reaching edge of the map
        
        g = [["-" for col in range(width)] for row in range(height)] #creates appropriate size for the map
        while rooms > 0:

            y = random.randint(offsetY, yRange)
            x = random.randint(offsetX, xRange)
            #generate random coordinates to create rooms

            try:
                index = doNotReuse.index((y, x))
                #if the index of (y, x) cannot be found then we *****CAN****** place a room there.
                
            except ValueError: #IF WE GET THIS ERROR THEN WE CAN PLACE A ROOM THERE

                #offsetY and offsetX are for the distance between the walls, refer to createRoom() for details
                createRoom(y, x, g, offsetY, offsetX)
                rooms = rooms - 1
                doNotReuse.append((y, x)) #add that coordinate to list because we can't place another room there

        for y in range(height):
            rocks = 2
            for x in range(width):
                #random.randint(a, b) = c determines % for a rock to be placed at (y, x) , 2 rocks total can be placed per line
                if random.randint(1, 50) == 10 and rocks > 0 and y % 2 == 0: #y must be an even number for rock to be placed on (y, x), done to not place rocks on every row
                    g[y][x] = "R"
                    rocks = rocks - 1
        return cls(g)

    @classmethod
    def random_individual(cls):
        #SAME EXACT METHOD AS jrod_individual, change it up as you see fit to add more variation to the starting population.
        offsetY = 10 

        offsetX = 10 
        #refer to createRoom() for details, these offsets are for when a room is generated it has the appropriate spacing
        #these offsets can be changed for different dimentions on the rooms 
        
        rooms = 7 #number of rooms to generate
        
        doNotReuse = [] #list of coordinates where you can't call createRoom()
        
        yRange = height - offsetY - 1
        xRange = width - offsetX - 1
        #we dont want the to place stuff on the coordinates at the edges, hence the offset, to prevent a horizontal wall from reaching edge of the map
        
        g = [["-" for col in range(width)] for row in range(height)] #creates appropriate size for the map
        while rooms > 0:

            y = random.randint(offsetY, yRange)
            x = random.randint(offsetX, xRange)
            #generate random coordinates to create rooms

            try:
                index = doNotReuse.index((y, x))
                #if the index of (y, x) cannot be found then we *****CAN****** place a room there.
                
            except ValueError: #IF WE GET THIS ERROR THEN WE CAN PLACE A ROOM THERE

                #offsetY and offsetX are for the distance between the walls, refer to createRoom() for details
                createRoom(y, x, g, offsetY, offsetX)
                rooms = rooms - 1
                doNotReuse.append((y, x)) #add that coordinate to list because we can't place another room there

        for y in range(height):
            rocks = 2
            for x in range(width):
                #random.randint(a, b) = c determines % for a rock to be placed at (y, x) , 2 rocks total can be placed per line
                if random.randint(1, 50) == 10 and rocks > 0 and y % 2 == 0: #y must be an even number for rock to be placed on (y, x), done to not place rocks on every row
                    g[y][x] = "R"
                    rocks = rocks - 1
        return cls(g)
        
        

# Inspired by https://www.researchgate.net/profile/Philippe_Pasquier/publication/220867545_Towards_a_Generic_Framework_for_Automated_Video_Game_Level_Creation/links/0912f510ac2bed57d1000000.pdf

Individual = Individual_Grid

def createRoom(y, x, genome, offsetY, offsetX):
        genome[y][x] = "H"
        genome[y + offsetY][x - offsetX] = "V"
        genome[y + offsetY][x + offsetX] = "V"
        #               H
        #
        #
        #
        #
        #
        # V                         V
        #this is what createRoom() generates, notice the offsets for x and y
        #(y, x) would be at the exact position as H
        #you can update this function to have rooms that aren't always facing a certain way
        
def genomeClear(genome):
    spawners = spawnPoints
    spawnCounter = 0
    for y in range(height):
        for x in range(width):
            if random.randint(1, 100) == 1 and y % 2 == 0: #make it a low chance of replacing (y, x) with "-"
                genome[y][x] = "-"
            elif genome[y][x] == "S":
                spawnCounter = spawnCounter + 1 
    
    if spawnCounter < 5:
        for y in range(height):
            for x in range(width):
                if random.randint(1, 800) == 1 and y % 2 != 0 and spawners > 0: #make it a low chance of replacing (y, x) with "S"
                    genome[y][x] = "S"
                    spawners = spawners - 1
                    
    return genome

def dijkstra_path_to_prefabs(initial_position, destinationList, genome, adj):
    # create a list of all coordinates in the graph except walls
    all_coordinates = []
    for y in range(height):
        for x in range(width):
            if genome[y][x] == "-" or genome[y][x] == "S":
                all_coordinates.append((y, x))
            
    
    # initialize pathcosts and parents
    pathcosts = {node: inf for node in all_coordinates}
    parents = {node: None for node in all_coordinates}

    #del all_coordinates  # not going to use again, so delete it for clarity

    pathcosts[initial_position] = 0

    queue = [(0, initial_position)]

    while queue:
        _, current_node = heappop(queue)
        for node, cost in adj(all_coordinates, current_node, genome):
            pathcost = cost + pathcosts[current_node]
            if pathcost < pathcosts[node]:
                pathcosts[node] = pathcost
                parents[node] = current_node
                heappush(queue, (pathcost, node))
    
    paths = []
    for coordinate in destinationList:
        reverse_path = [coordinate]
        while parents[reverse_path[-1]] is not None:
            reverse_path.append(parents[reverse_path[-1]])
        paths.append(reverse_path[::-1])
            
    return paths

def adj(all_coordinates, current_node, genome):
    adjList = []
    #(y, x)
    #top cell
    try:
        topCell = (current_node[0] - 1, current_node[1])
        index = all_coordinates.index(topCell)
        eDistance(genome, topCell, current_node, adjList)
    except ValueError:
        #cell doesn't exist don't add to list
        pass
    
    #bottom cell
    try:
        bottomCell = (current_node[0] + 1, current_node[1])
        index = all_coordinates.index(bottomCell)
        eDistance(genome, bottomCell, current_node, adjList)
    except ValueError:
        #cell doesn't exist don't add to list
        pass

    #left cell
    try:
        leftCell = (current_node[0], current_node[1] - 1)
        index = all_coordinates.index(leftCell)
        eDistance(genome, leftCell, current_node, adjList)
    except ValueError:
        #cell doesn't exist don't add to list
        pass

    #right cell
    try:
        rightCell = (current_node[0], current_node[1] + 1)
        index = all_coordinates.index(rightCell)
        eDistance(genome, rightCell, current_node, adjList)
    except ValueError:
        #cell doesn't exist don't add to list
        pass
        
    #((y, x), cost)
    return adjList

def eDistance(genome, cell, current_node, adjList):
    if genome[cell[0]][cell[1]] == "-" or genome[cell[0]][cell[1]] == "S":
            xDist = (cell[1] - current_node[1]) ** 2
            yDist = (cell[0] - current_node[0]) ** 2
            eDist = sqrt(xDist + yDist)
            adjList.append((cell, eDist))
    
def generate_successors(population):

    results = []

    # Roulette Wheel Selection
    normalize_pop = {}
    probability = {}
    fitness_sum = 0
    min_fitness = abs(min([key.fitness() for key in population]))

    for node in population:
        normalize_pop[node] = node.fitness() + min_fitness + 0.20
        fitness_sum += normalize_pop[node]

    normalize_sorted_list = sorted(normalize_pop.items(), key=lambda item: item[1])
    normalize_sorted = {}

    for node in normalize_sorted_list:
        normalize_sorted[node[0]] = node[1]

    last_probability = 0
    for node in population:
        prob = last_probability + (normalize_sorted[node] / fitness_sum)
        probability[node] = prob
        last_probability = prob

    pop_size = len(population)
    for i in range(pop_size):

        random_num = random.uniform(0, 1)
        selected_parent1 = population[0]
        for key in probability:
            if probability[key] > random_num:
                selected_parent1 = key
                break

        random_num = random.uniform(0, 1)
        selected_parent2 = population[0]
        for key in probability:
            if probability[key] > random_num:
                selected_parent2 = key
                break

        results.append(Individual.generate_children(selected_parent1, selected_parent2)[0])

    return results


def fileToWorld(f):
    genome = [[0 for j in range(0, 200)] for i in range(0, 16)]
    y = 0
    xGrid = 0
    for lines in f:
        for step in range(0, 200):
            genome[y][step] = lines[step]
        y = y + 1
    INDipop = Individual_Grid(genome)
    return INDipop

def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 100
    # Code to parallelize some computations
    batches = os.cpu_count()
    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))
    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()
        # STUDENT (Optional) change population initialization
        
        population = [Individual.random_individual() if random.random() < 0.9
                      else Individual.jrod_individual()
                      for _g in range(pop_limit)]
        
        # But leave this line alone; we have to reassign to population because we get a new population that has more cached stuff in it.
        population = pool.map(Individual.calculate_fitness,
                              population,
                              batch_size)
        init_done = time.time()
        print("Created and calculated initial population statistics in:", init_done - init_time, "seconds")
        generation = 0
        start = time.time()
        now = start
        print("Use ctrl-c to terminate this loop manually.")
        try:
            while True:
                now = time.time()
                # Print out statistics
                if generation > 0:
                    
                    #Taking the best individual and creating a path to specific prefabs, outputting that path on the map
                    best = max(population, key=Individual.fitness)
                    bestGenome = best.to_level()
                    destinationPrefabs = []


                    # Adding 2 rooms in the map randomly
                    random1 = (random.randint(9, height - 9), random.randint(9, width - 9))
                    random2 = (random.randint(9, height - 9), random.randint(9, width - 9))

                    bestGenome[random1[0]][random1[1]] = "J"
                    bestGenome[random2[0]][random2[1]] = "J"

                    for y in range(-9, 10):
                        for x in range(-7, 8):
                            if y == 0 and x == 0:
                                pass
                            else:
                                bestGenome[random1[0] + y][random1[1] + x] = "o"
                                bestGenome[random2[0] + y][random2[1] + x] = "o"
                    
                    for y in range(height):
                        for x in range(width):
                            if bestGenome[y][x] == "S": #the prefabs whose path we want to calculate
                                destinationPrefabs.append((y, x))
                   
                    #calculates a path from the initial point (y, x) to the prefabs
                    #currently set to the middle of graph (42, 50)
                    allPaths = dijkstra_path_to_prefabs((42, 50), destinationPrefabs, bestGenome, adj)
                    
                    for paths in allPaths: #allPaths = [path1, path2, path3] where path1 = [(y, x), (y, x)]
                        for coordinates in paths: #coordinates = (y, x)
                            try:
                                index = destinationPrefabs.index(coordinates) #This is here so we don't delete our destination prefab
                            except ValueError:
                                bestGenome[coordinates[0]][coordinates[1]] = "X" #replace genome[y][x] with an X
                    
                    best.replaceGenome(bestGenome)


                    
                    #best's genome now has an updated path to prefabs
                    
                    print("Generation:", str(generation))
                    print("Max fitness:", str(best.fitness()))
                    print("Average generation time:", (now - start) / generation)
                    print("Net time:", now - start)
                    with open("levels/last.txt", 'w') as f:
                        for row in best.to_level():
                            f.write("".join(row) + "\n")
                generation += 1
                # STUDENT Determine stopping condition
                stop_condition = False
                if stop_condition:
                    break
                # STUDENT Also consider using FI-2POP as in the Sorenson & Pasquier paper
                gentime = time.time()
                next_population = generate_successors(population)
                gendone = time.time()
                print("Generated successors in:", gendone - gentime, "seconds")
                # Calculate fitness in batches in parallel
                next_population = pool.map(Individual.calculate_fitness,
                                           next_population,
                                           batch_size)
                popdone = time.time()
                print("Calculated fitnesses in:", popdone - gendone, "seconds")
                population = next_population
        except KeyboardInterrupt:
            pass
    return population


if __name__ == "__main__":
    final_gen = sorted(ga(), key=Individual.fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness: " + str(best.fitness()))
    now = time.strftime("%m_%d_%H_%M_%S")
    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...
    for k in range(0, 10):
        with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
            for row in final_gen[k].to_level():
                f.write("".join(row) + "\n")

    #path = "levels/last.txt"
    #shutil.copy(path, "Josue Uriarte\Documents\Game_AI_Project/Assets/Maps/last.txt")
    #C:\Users\Josue
    #Uriarte\Documents\Game_AI_Project\Assets\Maps