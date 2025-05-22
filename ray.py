from pygame.math import Vector3

class ray:
    def __init__(self, origin=(0,0,0), direction=(0,0,0)):
        self.origin = Vector3(origin)
        self.direction = Vector3(direction)
    
    def __str__(self):
        return f"{self.origin}{self.direction}"
    
    def at(self, t):
        return self.origin + t*self.direction
