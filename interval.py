from math import inf as infinity
import pygame.math as pmath

class interval:
    def __init__(self, min=infinity, max=-infinity):
        self.min = min
        self.max = max
    
    def contains(self,x):
        return (self.min <= x and x <= self.max)
    
    def surrounds(self,x):
        return (self.min < x and x < self.max)

    def clamp(self,x):
        return pmath.clamp(x,self.min,self.max)
