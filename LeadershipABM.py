from random import randint, uniform
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

    # A list of animals, each having their own individual parameters of name, position, direction, and speed
    # creating a list with all the respective parameters
    animal_list = []
    for num in range(0, num_animals):
        rand_speed = 1  # For now, setting the speed of all the animals in the list to 1
        animal_list.append(Animal('ANIMAL' + str(num), [uniform(0, 10), uniform(0, 10)], randomDirection(), rand_speed))

    print(animal_list)
    print(animal_list[1].position)
    animal_list[1].move(animal_list, alpha)
    print(animal_list[1].position)
    print(animal_list)


# Creating an object called Animal
class Animal:
    def __init__(self, name, position, direction, speed=0):
        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed

    def getNeighborVectors(self, neighbor_list):
        vectors = [np.subtract(o.position, self.position) for o in neighbor_list]
        return vectors

    def move(self, animal_list, alpha):
        neighbor_list = animal_list
        neighbor_list.remove(self)
        neighbor_vectors = self.getNeighborVectors(neighbor_list)
        within_alpha = [v for v in neighbor_vectors if getHypotenuse(v) < alpha]
        if len(within_alpha) > 0:
            unit_vectors = [None] * len(within_alpha)
            for i in range(len(within_alpha)):
                unit_vectors[i] = unitVectorize(within_alpha[i])
            self.direction = unitVectorize(-1 * sum(unit_vectors))
            self.position = self.direction * self.speed + self.position
        else:
            print("attraction")
            self.attraction(neighbor_vectors, neighbor_list)

    def attraction(self, neighbor_vectors, neighbor_list):
        self.direction = unitVectorize(unitVectorize(sum(neighbor_vectors)) + np.sum(getDirections(neighbor_list)))
        self.position = self.direction * self.speed + self.position

class informedAnimal(Animal):
    def __init__(self, name, position, direction, speed=0, omega):
        Animal.__init__(self, name, position, direction, speed=0)
        self.speed = speed
        self.omega = omega

    def informedAttraction(self, neighbor_vectors, neighbor_list, direction, omega):
        targetDestination = [uniform(0, 10), uniform(0, 10)]
        self.direction = [np.subtract(targetDestination, self.position)] + omega*unitVectorize(direction)/unitVectorize([np.subtract(targetDestination, self.position)] + omega*unitVectorize(direction))

# This small function helps us determine the x and y direction vectors. This will be a unit vector.
def randomDirection():
    radians = uniform(0, 2 * pi)
    return [cos(radians), sin(radians)]


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
