from random import randint, uniform, random, choice
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from math import acos, sin, cos, degrees, atan2
from math import sqrt


def main():
    # The user inputs the number of Animal Objects
    num_animals = input("Please enter the number of Animals: ")
    num_animals = int(num_animals)

    # The user inputs the alpha (the minimum distance value)
    alpha = input("Please enter the alpha: ")
    alpha = float(alpha)

    # The user inputs the alpha (the minimum distance value)
    num_targets = input("Please enter the number of targets: ")
    num_targets = int(num_targets)

    # The user inputs the error
    error = input("Please enter the error: ")
    error = float(error)

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animal_list = []
    for num in range(0, num_animals):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        target = [0,0]
        animal_list.append(Animal('ANIMAL' + str(num), [uniform(-5, 5), uniform(-5, 5)], randomDirection(), rand_speed, target))

    targetDestination_list = []
    for num in range(0, num_targets):
        targetDestination_list.append(Target('TARGET' + str(num), [uniform(0, 10), uniform(0, 10)]))

    print(animal_list)
    print(targetDestination_list[1].name)
    print(animal_list[1].position)
    animal_list[1].move(animal_list, alpha)
    print(animal_list[1].position)
    print(animal_list)


# Creating an object called Animal
class Animal:
    def __init__(self, name, position, direction, speed, target, error):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed
        self.target = target
        self.error = error

    def getNeighborVectors(self, neighbor_list):
        vectors = [np.subtract(o.position, self.position) for o in neighbor_list]
        return vectors

    def move(self, animal_list, alpha, error):
        neighbor_list = animal_list.copy()
        neighbor_list.remove(self)
        neighbor_vectors = self.getNeighborVectors(neighbor_list)
        within_alpha = [v for v in neighbor_vectors if getHypotenuse(v) < alpha]
        if len(within_alpha) > 0:
            unit_vectors = [None] * len(within_alpha)
            for i in range(len(within_alpha)):
                unit_vectors[i] = unitVectorize(within_alpha[i])
            self.direction = unitVectorize(-1 * sum(unit_vectors))*uniform(0,error)
            self.position = self.direction * self.speed + self.position*uniform(0,error)
        else:
            print("attraction")
            self.attraction(neighbor_vectors, neighbor_list)

    def attraction(self, neighbor_vectors, neighbor_list):
        self.direction = unitVectorize(unitVectorize(sum(neighbor_vectors)) + np.sum(getDirections(neighbor_list)))
        self.position = self.direction * self.speed + self.position

class informedAnimal(Animal):
    def __init__(self, name, position, direction, speed, omega, informedAnimalList, targetDirection = None):
        Animal.__init__(self, name, position, direction, speed)
        self.omega = omega
        self.target = target

    def attraction(self, neighbor_vectors, neighbor_list, omega, informedAnimalList, targetList):
        if (target == None):
            self.target = choice(targetList).position
        targetDirection = getInformedDirection(informedAnimalList, targetList)

        self.direction = unitVectorize(unitVectorize(sum(neighbor_vectors)) + np.sum(getDirections(neighbor_list)))
        self.direction = self.direction + omega

class Target:
    def __init__(self, name, position = None):
        self.name = name
        self.position = position

        if(position = None):
            self.position = choice([-1,1],2)*[uniform(5, 20), uniform(5, 20)]
        self.position = position


# This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0, 2 * pi)
    return [cos(radians), sin(radians)]

# this small function helps us determine the coordinates of each animal
def getPositions(animal_list):
    return [o.position for o in animal_list]

def getDirections(animal_list):
    return [o.direction for o in animal_list]

def getInformedDirection(informedAnimalList, targetList):
    return ((informedAnimalList[0] - targetList[0]) ** 2 + (informedAnimalList[1] - targetList[1] ** 2)) **0.5

# this small function returns the distances of the other animals to a chosen animal
def getHypotenuse(movement_vector):
    return (movement_vector[0] ** 2 + movement_vector[1] ** 2) ** 0.5

def unitVectorize(vector):
    magnitude = getHypotenuse(vector)
    return vector / magnitude

main()
