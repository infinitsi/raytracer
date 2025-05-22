from copy import *
from hittable import *
from interval import *

class hittable_list(hittable):
    def __init__(self):
        self.objects = []
    
    def clear(self):
        self.objects.clear()
    
    def add(self, object):
        self.objects.insert(0,object)
    
    def hit(self, r, ray_t, rec):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = ray_t.max
        
        for obj in self.objects:
            if(obj.hit(r, interval(ray_t.min, closest_so_far), temp_rec)):
                hit_anything = True
                closest_so_far = copy(temp_rec.t)
                rec.p = temp_rec.p
                rec.t = temp_rec.t
                rec.front_face = temp_rec.front_face
                rec.normal = temp_rec.normal
                rec.mat = temp_rec.mat
        return hit_anything
