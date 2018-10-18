from random import randint, uniform
import collections
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from math import acos, sin, cos, degrees, atan2
from math import sqrt

# Creating an object called Animal
class Animal:
    def __init__(self, name, position, direction, speed=0):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed

    def getNeighborVectors(self, animalList):
        vectors = [np.subtract(o.position, self.position) for o in animalList]
        return vectors

#This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0 ,2*pi)
    return [cos(radians), sin(radians)]

#creating a list with all the respective parameters

def main():
    # The user inputs the number of Animal Objects
    num_animals = input("Please enter the number of Animals: ")
    num_animals = int(num_animals)
    animalList = []
    for num in range(0, num_animals):
        randSpeed = 1  # For now, setting the speed of all the animals in the list to 1
        animalList.append(Animal('ANIMAL' + str(num), [uniform(0, 10), uniform(0, 10)], randomDirection(), randSpeed))
    print(animalList[1].getNeighborVectors(animalList))
    return animalList[1].getNeighborVectors(animalList)

if __name__ == '__main__':
    main()




