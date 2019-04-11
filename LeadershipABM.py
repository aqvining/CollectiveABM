from random import randint, uniform, random, choice
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from matplotlib import animation
from math import acos, sin, cos, degrees, atan2
from math import sqrt
import time


def main():

    # The user inputs the number of uninformed Animal Objects
    # num_uninformed = input("Please enter the number of uninformed Animals: ")
    # num_uninformed = int(num_uninformed)
    num_uninformed = 10

    # The user inputs the number of uninformed Animal Objects
    # num_informed = input("Please enter the number of informed Animals: ")
    # num_informed = int(num_informed)
    num_informed = 1

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
    error = 0.5

    # The user inputs the number of time steps
    # steps = input("Please enter the number of steps for which the simulation should run: ")
    # steps = int(steps)
    steps = 100
    all_positions = dict()

    targetDestination_list = []
    for num in range(0, num_targets):
        targetDestination_list.append(Target('TARGET' + str(num)))

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animal_list = []

    for num in range(num_informed): #descriptive arguments
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(informedAnimal('Informed' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, error, omega, targetDestination_list))

    for num in range(num_uninformed):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(Animal('Uninformed' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, error))



    agentNames = [o.name for o in animal_list]
    all_agents = {i: list() for i in agentNames}


    for i in range(steps):
        all_positions[i] = [o.position for o in animal_list]
        for o in animal_list:
            all_agents[o.name].append(o.position)
        for animal in animal_list:
            animal.move(animal_list, alpha)
        for animal in animal_list:
            animal.position = animal.new_position
            animal.direction = animal.new_direction
    print(all_positions)
    print(all_agents)
    #return(all_positions)
    return (all_positions, all_agents, targetDestination_list)



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

# This is the Target class. A target is a named point, outside the distribution of animals with a uniform and random distribution.
class Target:
    def __init__(self, name, position=None):
        self.name = name
        self.position = position

        if self.position is None:
            self.position = np.random.choice([-1,1],size=2)*[uniform(5, 20), uniform(5, 20)]


# This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0, 2 * pi)
    return np.array([cos(radians), sin(radians)])

# this small function helps us determine the coordinates of each animal
def getPositions(animal_list):
    return [o.position for o in animal_list]

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




run = main()
#plotTimestep(run[0], 1)

fig = plt.figure()
ax = plt.axes(xlim=(-20, 20), ylim=(-20,20))
paths = [plt.plot([], [])[0] for _ in range(len(run[1]))]
target_x = [target.position[0] for target in run[2]]
target_y = [target.position[1] for target in run[2]]
target = ax.scatter(target_x,target_y)
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
    x = [target.position[0] for target in run[2]]
    y = [target.position[1] for target in run[2]]
    plt.scatter(x,y)
    return paths

anim = animation.FuncAnimation(fig, animate, init_func = animate_init, frames = len(run[0]), interval = 100, blit = True)
anim.save('collective_animation.gif', writer='imagemagick', fps=60)
plt.show()