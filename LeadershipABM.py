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
import pickle
import time
import pickle


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
    omega = 0.5

    # The user inputs the alpha (the minimum distance value)
    # alpha = input("Please enter the alpha: ")
    #alpha = float(alpha)
    alpha = 1

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

    steps = 500


    all_positions = dict()

    targetDestination_list = []
    for num in range(0, num_targets):
        targetDestination_list.append(Target('TARGET' + str(num)))

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
    all_elongation = {i: list() for i in range (0,steps)}

    agentNames = [o.name for o in animal_list]
    all_agents = {i: list() for i in agentNames}
    for i in range(steps):
        all_positions[i] = [o.position for o in animal_list]
        all_directions[i] = [o.direction for o in animal_list]
        for o in animal_list:
            all_agents[o.name].append(o.position)
        for animal in animal_list:
            animal.move(animal_list, alpha)
        for animal in animal_list:
            animal.position = animal.new_position
            animal.direction = animal.new_direction



    groupDirection = np.subtract(getCentroid(all_positions[steps-1]), getCentroid(all_positions[50]))
    for i in range(steps):
        all_elongation[i] = getElongation(all_positions[i], groupDirection)

    s = getMeanAngularDev(all_directions,groupDirection)

    return (all_positions, all_agents, all_directions, all_elongation, normalize(s))


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
        if self.target is None:
            self.target = choice(self.target_list).position
        targetDirection = unitVectorize(np.subtract(self.target, self.position))

        self.new_direction = unitVectorize(sum(neighbor_vectors) + sum(getDirections(neighbor_list)))
        self.new_direction = unitVectorize(self.new_direction + self.omega * targetDirection)
        # self.new_direction = atan2(self.new_direction[1], self.new_direction[0]) + self.error


# This is the Target class. A target is a named point, outside the distribution of animals with a uniform and random distribution.
class Target:
    def __init__(self, name, position=None):
        self.name = name
        self.position = position

        if (self.position is None):
            self.position = np.multiply(randomDirection(), 10000)



# This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0, 2 * pi)
    return np.array([cos(radians), sin(radians)])

# this small function helps us determine the coordinates of each animal
def getPositions(animal_list):
    return [o.position for o in animal_list]

def getCentroid(positions):
    x_coords = [p[0] for p in positions]
    y_coords = [p[1] for p in positions]
    _len = len(positions)
    centroid_x = sum(x_coords) / _len
    centroid_y = sum(y_coords) / _len
    centroid = [centroid_x, centroid_y]
    return centroid

def getElongation(positions, direction):
    centroid = getCentroid(positions)
    direction_point = np.sum([direction, centroid], axis=0)
    wdistances = [getDistFromLine(centroid, direction_point, position) for position in positions]
    perpendicular_point = [centroid[0]-direction_point[1], direction_point[0]+centroid[1]]
    ldistances = [getDistFromLine(centroid, perpendicular_point, position) for position in positions]

    elongation = (max(ldistances) - min(ldistances))/(max(wdistances) - min(wdistances))

    return elongation


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


def getMeanAngularDev(all_directions,groupDirection):
    complete_directions = []
    for key in all_directions.keys():
        complete_directions += all_directions[key]
    groupAngle = atan2(groupDirection[1], groupDirection[0])
    angularDev =  [groupAngle - atan2(direction[1], direction[0]) for direction in complete_directions]

    A = 0
    B = 0

    for a in angularDev:
        A += cos(a)
        B += sin(a)
    A = A/len(complete_directions)
    B = B/len(complete_directions)
    r = sqrt(A**2+B**2)
    s = sqrt(2*(1-r))
    return s

def normalize(s):
    return abs(s - pi)/pi

#run = main(10,1)
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



all_data = {10:{},30:{},50:{},100:{}} #initializing a list with size 5 because N = 10,30,50,100, 200 in Couzin paper
filehandler = open("simulation.pkl", 'wb')

for N in [10, 30, 50, 100]:
    print("Entering: N = ", N)
    for I in range(1, N+1):
        all_data[N][I] = main(N, I)
        print("Completed I = ", I)
    filehandler = open("simulation" + str(N) + ".pkl", 'wb')
    pickle.dump(all_data[N], filehandler)
    filehandler.close()




def plotAccuracy(all_data):
    #plt.figure()
    i=0
    for N in all_data.keys():
        x = []
        y = []
        for I in all_data[N].keys():
            x.append(I/N)
            y.append(all_data[N][I][4])
        col = ["black", "blue", "green", "yellow"][i]
        plt.plot(x, y, color = col)
    i += 1
    plt.suptitle('Group Accuracy vs. Proportion of Informed Individuals', fontsize=20)
    plt.xlabel('Proportion of Informed Individuals', fontsize=18)
    plt.ylabel('Group Accuracy', fontsize=16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.show()

def plotElongation(all_data):
    #plt.figure()
    for N in all_data.keys():
        x = []
        y = []
        for I in all_data[N].keys():
            x.append(I/N)
            elongations = all_data[N][I][3]
            y.append(statistics.mean(elongations[key] for key in elongations))
        plt.plot(x, y)
    plt.suptitle('Group Elongation vs. Proportion of Informed Individuals', fontsize=20)
    plt.xlabel('Proportion of Informed Individuals', fontsize=18)
    plt.ylabel('Group Elongation', fontsize=16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.show()


#plotAccuracy(all_data)
#plotElongation(all_data)
def animate_init():
    for path in paths:
        path.set_data([],[])
    return paths

def animate(i):
    k = i-4
    if k<0:
        k = 0
    for j, agent in enumerate(run[1]):
        x = [position[0] for position in run[1][agent][k:i]]
        y = [position[1] for position in run[1][agent][k:i]]
        paths[j].set_data(x,y)
    #x = [target.position[0] for target in run[2]]
    #y = [target.position[1] for target in run[2]]
    #plt.scatter(x,y)
    return paths

run = main(10,1)
#plotTimestep(run[0], 1)

fig = plt.figure()
ax = plt.axes(xlim=(-20, 20), ylim=(-20,20))
paths = [plt.plot([], [])[0] for _ in range(len(run[1]))]
#target_x = [target.position[0] for target in run[2]]
#target_y = [target.position[1] for target in run[2]]
#target = ax.scatter(target_x,target_y)


anim = animation.FuncAnimation(fig, animate, init_func = animate_init, frames = len(run[0]), interval = 100, blit = True)
#anim.save('collective_animation_1-50.gif', writer='imagemagick', fps=60)
plt.show()

plt.show()

