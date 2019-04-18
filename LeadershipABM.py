from random import randint, uniform, random, choice
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from matplotlib import animation
from math import acos, sin, cos, degrees, atan2
import scipy.stats as ss
import statistics
from math import sqrt
import time

def main(N,I):

    # The user inputs the number of uninformed Animal Objects
    # num_uninformed = input("Please enter the number of uninformed Animals: ")
    # num_uninformed = int(num_uninformed)
    num_uninformed = N-I

    # The user inputs the number of uninformed Animal Objects
    # num_informed = input("Please enter the number of informed Animals: ")
    # num_informed = int(num_informed)
    #num_informed = 1
    num_informed = I

    #The user inputs omega (strength of target direction on informed movement, between 0 and 1)
    # omega = float(input("Please enter the omega value for informed Animals: "))
    omega = 1

    # The user inputs the alpha (the minimum distance value)
    # alpha = input("Please enter the alpha: ")
    #alpha = float(alpha)
    alpha = 0.1

    # The user inputs the alpha (the minimum distance value)
    # num_targets = input("Please enter the number of targets: ")
    # num_targets = int(num_targets)
    num_targets = 1

    # The user inputs the error
    # error = input("Please enter the standard deviation of movement error: ")
    # error = float(error)
    #error = 0.5


    # The user inputs the number of time steps
    # steps = input("Please enter the number of steps for which the simulation should run: ")
    # steps = int(steps)
    steps = 100

    all_positions = dict()

    targetDestination_list = []
    for num in range(0, num_targets):
        targetDestination_list.append(Target('TARGET' + str(num), [uniform(5, 10), uniform(5, 10)]))

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animal_list = []

    for num in range(num_informed): #descriptive arguments
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(informedAnimal('Informed' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, ss.vonmises.rvs(10000, size = 1), omega, targetDestination_list))

    for num in range(num_uninformed):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(Animal('Uninformed' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, ss.vonmises.rvs(10000, size = 1)))


    all_directions = {i: list() for i in range(0, steps)}

    agentNames = [o.name for o in animal_list]
    all_agents = {i: list() for i in agentNames}
    for i in range(steps):
        all_positions[i] = [o.position for o in animal_list]
        all_directions[i] = np.sum([o.direction for o in animal_list], axis=0)
        for o in animal_list:
            all_agents[o.name].append(o.position)
        for animal in animal_list:
            animal.move(animal_list, alpha)
        for animal in animal_list:
            animal.position = animal.new_position
            animal.direction = animal.new_direction

    return (all_positions, all_agents, all_directions)



# Creating an object called Animal. All animals have a name, position, inherent direction and speed.
class Animal:
    def __init__(self, name, position, direction, speed, error):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed
        self.error = error
        self.new_direction = None

    def getNeighborVectors(self, neighbor_list):
        vectors = [np.subtract(o.position, self.position) for o in neighbor_list]
        return vectors

    def move(self, animal_list, alpha):
        neighbor_list = animal_list.copy()
        neighbor_list.remove(self)
        neighbor_vectors = self.getNeighborVectors(neighbor_list)
        within_alpha = [v for v in neighbor_vectors if getHypotenuse(v) < alpha]
        if len(within_alpha) > 0:
            unit_vectors = [None] * len(within_alpha)
            for i in range(len(within_alpha)):
                unit_vectors[i] = unitVectorize(within_alpha[i])
            self.new_direction = unitVectorize(-1 * sum(unit_vectors))
        else:
            self.attraction(neighbor_vectors, neighbor_list)
        # self.new_direction = atan2(self.new_direction[1], self.new_direction[0]) + self.error
        self.new_position = self.new_direction * self.speed + self.position

    def attraction(self, neighbor_vectors, neighbor_list):
       self.new_direction = unitVectorize(sum(neighbor_vectors) + sum(getDirections(neighbor_list)))


# informed animals are a subclass of Animal. They know a the positions and names of targets.
# in addition to the knowledge of targets, informed animals also have the ability to draw the other animals in the group
# with a strength term (omega)

class informedAnimal(Animal):
    def __init__(self, name, position, direction, speed, error, omega, target_list):
        Animal.__init__(self, name, position, direction, speed, error)
        self.omega = omega
        self.target_list = target_list
        self.target = None

    def attraction(self, neighbor_vectors, neighbor_list):
        if (self.target == None):
            self.target = choice(self.target_list).position
        targetDirection = unitVectorize(np.subtract(self.target, self.position))

        self.new_direction = unitVectorize(sum(neighbor_vectors) + sum(getDirections(neighbor_list)))
        self.new_direction = unitVectorize(self.new_direction + self.omega * targetDirection)
        # self.new_direction = atan2(self.new_direction[1], self.new_direction[0]) + self.error


# This is the Target class. A target is a named point, outside the distribution of animals with a uniform and random distribution.
class Target:
    def __init__(self, name, position = None):
        self.name = name
        self.position = position

        if (position == None):
            self.position = choice([-1,1],2)*[uniform(5, 20), uniform(5, 20)]
        self.position = position


# This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0, 2 * pi)
    return np.array([cos(radians), sin(radians)])

# this small function helps us determine the coordinates of each animal
def getPositions(animal_list):
    return [o.position for o in animal_list]

def getElongation(positions, direction):
    x_coords = [p[0] for p in positions]
    y_coords = [p[1] for p in positions]
    _len = len(positions)
    centroid_x = sum(x_coords) / _len
    centroid_y = sum(y_coords) / _len
    centroid = [centroid_x, centroid_y]

    direction_point = np.sum([direction, centroid], axis=0)
    wdistances = [getDistFromLine(centroid, direction_point, position) for position in positions]
    perpendicular_point = [centroid[0]-direction_axis[1], direction_axis[0]+centroid[1]]
    ldistances = [getDistFromLine(centroid, perpendicular_point, position) for position in positions]


def getDistFromLine(p1, p2, p3):   ##p1 and p2 are points on the line
    dist = ((p2[0]-p1[0])*(p1[1]-p3[1]) - (p1[0]-p3[0])*(p2[1]-p1[1]))/np.sqrt(np.square(p2[0]-p1[0])+np.square(p2[1]-p1[1]))
    #if (p3[1]<p1[1]+(p1[0]-p3[0])*((p2[1]-p1[1])/(p2[0]-p1[0]))):
        #return dist * -1
    return dist





# this small function helps us determine the inherent direction of each animal in animalList
def getDirections(animal_list):
    return [o.direction for o in animal_list]

# this small function returns the distances of the other animals to a chosen animal
def getHypotenuse(movement_vector):
    return (movement_vector[0] ** 2 + movement_vector[1] ** 2) ** 0.5
# this small function unit vectorises its input vector
def unitVectorize(vector):
    magnitude = getHypotenuse(vector)
    return vector / magnitude
def plotTimestep(all_positions,key):
    x = [o[0] for o in all_positions[key]]
    y = [o[1] for o in all_positions[key]]
    plt.scatter(x, y)
    plt.show()

def plotAgents(all_agents,key):
    x = [o[0] for o in all_agents[key]]
    y = [o[1] for o in all_agents[key]]
    plt.plot(x,y)
    plt.show()

def allGraphs(all_positions, steps):
    for i in range(steps):
        plotTimestep(all_positions, i)




# run = main()
# #plotTimestep(run[0], 1)
#
# fig = plt.figure()
# ax = plt.axes(xlim=(-5, 10), ylim=(-5,10))
# paths = [plt.plot([], [])[0] for _ in range(len(run[1]))]
#
# def animate_init():
#     for path in paths:
#         path.set_data([],[])
#     return paths
#
# def animate(i):
#     for j, agent in enumerate(run[1]):
#         x = [position[0] for position in run[1][agent][:i]]
#         y = [position[1] for position in run[1][agent][:i]]
#         paths[j].set_data(x,y)
#     return paths

# def numLeaders(numAnimals, start, stop, step=1):
#     n = int(round((stop - start)/float(step)))
#     if n > 1:
#         step = ([start + step*i for i in range(n+1)])
#         numInformed = [numAnimals * x for x in step]
#         numInformed = np.round(numInformed, 2)
#         numInformed = np.int_(numInformed)
#         return(numInformed)
#     elif n == 1:
#         step = (([start]))
#         numInformed = [numAnimals * x for x in step]
#         numInformed = np.round(numInformed, 2)
#         numInformed = np.int_(numInformed)
#         return(numInformed)
#     else:
#         step = ([])
#         numInformed = [numAnimals * x for x in step]
#         numInformed = np.round(numInformed, 2)
#         numInformed = np.int_(numInformed)
#         return(numInformed)

##all_data = {10:{},30:{},50:{},100:{},200:{}} #initializing a list with size 5 because N = 10,30,50,100, 200 in Couzin paper


##for N in [10,30,50,100,200]:
##    print("Entering: N = ", N)
##    for I in range(1,N+1):
##        all_data[N][I] = main(N, I)




# anim = animation.FuncAnimation(fig, animate, init_func = animate_init, frames = len(run[0]), interval = 500, blit = True)
#
# plt.show()