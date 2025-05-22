from ray import *
from material import *

class hit_record:
    p = Vector3()
    normal = Vector3()
    mat = material()
    t = float()
    front_face = bool()
        
    def set_face_normal(self, r, outward_normal):
        self.front_face = (r.direction*outward_normal<0)
        self.normal = outward_normal if self.front_face else -outward_normal
        # self.normal = outward_normal

class hittable:
    def hit(self, r, ray_t, rec):
        return bool()
