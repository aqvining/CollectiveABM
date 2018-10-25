from random import randint, uniform
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from math import acos, sin, cos, degrees, atan2
from math import sqrt

def main ():
    # The user inputs the number of Animal Objects
    numAnimals = input("Please enter the number of Animals: ")
    numAnimals = int(numAnimals)

    # The user inputs the alpha (the minimum distance value)
    alpha = input("Please enter the alpha: ")
    alpha = float(alpha)

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animalList = []
    for num in range(0, numAnimals):
        randSpeed = 1  # For now, setting the speed of all the animals in the list to 1
        animalList.append(Animal('ANIMAL' + str(num), [uniform(0, 10), uniform(0, 10)], randomDirection(), randSpeed))

    print(animalList)
    print(animalList[1].getNeighborDistances(animalList))
    print(animalList[1].position)
    animalList[1].move(animalList, alpha)
    print(animalList[1].position)

    # animalList[1].getNeighborVectors(animalList)


# Creating an object called Animal
class Animal:
    def __init__(self, name, position, direction, speed=0):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed

    #def getUserInputs(self, numAnimals, alpha):

    def getNeighborDistances(self, animalList):
        vectors = [np.subtract(o.position, self.position) for o in animalList]
        return getHypotenuse(vectors)

    def getNeighborVectors(self, animalList):
        vectors = [np.subtract(o.position, self.position) for o in animalList]
        return vectors

    def move(self, animalList, alpha):
        neighborDistances = self.getNeighborDistances(animalList)
        if(sum(neighborDistances)< alpha) > 1:
            repulsingNeighbors = self.getNeighborVectors(animalList)[neighborDistances<alpha & neighborDistances!= 0]
            unitVectors = []*len(repulsingNeighbors)
            for i in range(0, len(repulsingNeighbors)):
                unitVectors[i] = unitVectorize(repulsingNeighbors[i])
            self.position = unitVectorize(-1*np.add(unitVectors))*self.speed + self.position


#This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0,2*pi)
    return [cos(radians), sin(radians)]

#this small function helps us determine the coordinates of each animal
def getPositions(animalList):
    return [o.position for o in animalList]

#this small function returns the distances of the other animals to a chosen animal
def getHypotenuse(movementVectors):
    return [(o[0] ** 2 + o[1] ** 2)** 0.5 for o in movementVectors]

def unitVectorize(vector):
    magnitude = getHypotenuse(vector)
    numerator = vector[0] ** 2 + vector[1] ** 2
    return numerator/magnitude





