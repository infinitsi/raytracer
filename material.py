from rtweekend import *


class material:
    emissionColor = Vector3(0,0,0)
    emissionStrength = 0
    def scatter(self, r_in, rec, attenuation, scattered):
        return False
    
    def __str__(self):
        return self.__class__.__name__

class lambertian(material):
    def __init__(self, albedo, emissionColor=(0,0,0), emissionStrength=0):
        self.albedo = Vector3(albedo)
        self.emissionColor = Vector3(emissionColor)
        self.emissionStrength = emissionStrength
    
    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + random_unit_vector()
        
        if(near_zero(scatter_direction)):
            scatter_direction = rec.normal
        
        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True

class metal(material):
    def __init__(self, albedo, fuzz):
        self.albedo = Vector3(albedo)
        self.fuzz = fuzz
    
    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = reflect(r_in.direction, rec.normal) + (self.fuzz * random_unit_vector())
        
        scattered.origin = rec.p
        scattered.direction = reflected
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return (scattered.direction * rec.normal > 0)

class dielectric(material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index
    
    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation.x = 1
        attenuation.y = 1
        attenuation.z = 1
        ri = (1/self.refraction_index if rec.front_face else self.refraction_index)
        
        unit_direction = Vector3.normalize(r_in.direction)
        cos_theta = min((-unit_direction*rec.normal), 1)
        sin_theta = (1 - cos_theta*cos_theta)**0.5
        
        cannot_refract = ri*sin_theta > 1
        direction = Vector3(0,0,0)
        
        if(cannot_refract or self.__reflectance(cos_theta,ri) > random()):
            direction = reflect(unit_direction,rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)
        
        scattered.origin = rec.p
        scattered.direction = direction
        return True
    
    def __reflectance(self, cosine, refraction_index):
        r0 = (1-refraction_index) / (1+refraction_index)
        r0 = r0*r0
        return r0 + (1-r0)*((1-cosine)**5)
