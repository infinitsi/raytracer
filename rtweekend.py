import math
from pygame.math import *
from random import random,uniform
from ray import *
from interval import *

infinity = math.inf
pi = math.pi

def degrees_to_radians(degrees):
    return degrees * pi / 180

# def random_double():
#     return random()

def random_vector(min=0, max=1):
    return Vector3(uniform(min,max),uniform(min,max),uniform(min,max))

def random_vector_in_unit_sphere():
    while True:
        p = random_vector(-1,1)
        if(p*p < 1):
            return p

def random_unit_vector():
    return Vector3.normalize(random_vector_in_unit_sphere())

def random_vector_on_hemisphere(normal):
    on_unit_sphere = random_unit_vector()
    if (on_unit_sphere*normal>0):
        return on_unit_sphere
    else:
        return -on_unit_sphere

def reflect(v,n):
    return Vector3.reflect(v,n)

def near_zero(v):
    s= 1e-06
    return (math.fabs(v.x)<s) and (math.fabs(v.y)<s) and (math.fabs(v.z)<s)

def refract(uv, n, etai_over_etat):
    cos_theta = min((-uv*n),1)
    r_out_perp = etai_over_etat * (uv + cos_theta*n)
    r_out_parallel = -math.sqrt(math.fabs(1 - r_out_perp*r_out_perp)) * n
    return r_out_perp + r_out_parallel
