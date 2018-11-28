from random import randint, uniform, random, choice
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from math import acos, sin, cos, degrees, atan2
from math import sqrt


def main():
    # The user inputs the number of uninformed Animal Objects
    num_uninformed = input("Please enter the number of uninformed Animals: ")
    num_uninformed = int(num_uninformed)

    # The user inputs the number of uninformed Animal Objects
    num_informed = input("Please enter the number of informed Animals: ")
    num_informed = int(num_informed)

    #The user inputs omega (strength of target direction on informed movement, between 0 and 1)
    omega = float(input("Please enter the omega value for informed Animals: "))

    # The user inputs the alpha (the minimum distance value)
    alpha = input("Please enter the alpha: ")
    alpha = float(alpha)

    # The user inputs the alpha (the minimum distance value)
    num_targets = input("Please enter the number of targets: ")
    num_targets = int(num_targets)

    # The user inputs the error
    error = input("Please enter the standard deviation of movement error: ")
    error = float(error)

    targetDestination_list = []
    for num in range(0, num_targets):
        targetDestination_list.append(Target('TARGET' + str(num), [uniform(0, 10), uniform(0, 10)]))

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animal_list = []

    for num in range(num_informed):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        target = [0,0]
        animal_list.append(informedAnimal('ANIMAL' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, error, omega, targetDestination_list))

    for num in range(num_uninformed):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(Animal('ANIMAL' + str(num), np.array([uniform(-5, 5), uniform(-5, 5)]), randomDirection(), rand_speed, error))


    print(animal_list)
    print(animal_list[1].position)
    for animal in animal_list:
        animal.move(animal_list, alpha)
    for animal in animal_list:
        animal.position = animal.new_position
        animal.direction = animal.new_direction

# Creating an object called Animal
class Animal:
    def __init__(self, name, position, direction, speed, error):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed
        self.error = error

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
        self.new_direction = unitVectorize(unitVectorize(sum(neighbor_vectors)) + np.sum(getDirections(neighbor_list)))

class informedAnimal(Animal):
    def __init__(self, name, position, direction, speed, error, omega, target_list):
        Animal.__init__(self, name, position, direction, speed, error)
        self.omega = omega
        self.target_list = target_list
        self.target = None

    def attraction(self, neighbor_vectors, neighbor_list):
        if (self.target == None):
            self.target = choice(self.target_list).position
        targetDirection = getHypotenuse(np.subtract(self.position, self.target))

        self.new_direction = unitVectorize(unitVectorize(sum(neighbor_vectors)) + np.sum(getDirections(neighbor_list)))
        self.new_direction = unitVectorize(self.new_direction + self.omega * targetDirection)

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

def getDirections(animal_list):
    return [o.direction for o in animal_list]

# this small function returns the distances of the other animals to a chosen animal
def getHypotenuse(movement_vector):
    return (movement_vector[0] ** 2 + movement_vector[1] ** 2) ** 0.5

def unitVectorize(vector):
    magnitude = getHypotenuse(vector)
    return vector / magnitude


main()
