from pygame.math import *
from math import *
from hittable import *

class sphere(hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, r, ray_t, rec):
        oc = self.center - r.origin
        a = r.direction*r.direction
        h = (r.direction*oc)
        c = oc*oc - self.radius*self.radius
        
        discriminant = h*h - a*c
        if discriminant<0:
            return False
        
        sqrtd = discriminant**0.5
        if(not a == 0):
            root = (h-sqrtd)/a
        else:
            root = 2*h*c
        if(not ray_t.surrounds(root)):
            if(not a == 0):
                root = (h+sqrtd)/a
            else:
                root = 2*h*c
            if(not ray_t.surrounds(root)):
                return False
        
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center)/self.radius
        rec.set_face_normal(r,outward_normal)
        rec.mat = self.mat
        
        return True
        
        #alt
        s = r.origin
        d = Vector3.normalize(r.direction)
        c = self.center
        rad = self.radius
        
        p = s - c
        
        rSquared = rad * rad
        p_d = p*d
        
        a = p - p_d * d
        aSquared = a*a
        
        h = (rSquared - aSquared)
        if(h < 0):
            return False
        h = h**0.5
        
        if(Vector3.dot(p,p)< rSquared):
            i = a+h*d
        else:
            i = a-h*d
        
        cis = c+i-s
        sgn = cis*r.direction
        if(sgn < 0):
            sgn = -1
        elif(sgn > 0):
            sgn = 1
        else:
            sgn = 0
        
        root = sgn * Vector3.magnitude(cis) / Vector3.magnitude(r.direction)
        if(not ray_t.surrounds(root)):
            return False
        
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center)/self.radius
        rec.set_face_normal(r,outward_normal)
        rec.mat = self.mat
        
        return True


        
        
