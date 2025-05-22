from rtweekend import *
from pygame.math import *
from pygame import Color
from pygame import display
from pygame import Surface
import pygame.pixelarray as pxarray
import pygame.gfxdraw as gfxdraw
from hittable import *
EPSILON = 1e-06


class camera:
    screenWidth = int()
    screenHeight = int()
    viewHeight = int()
    samples_per_pixel = 1
    pixel_samples_scale = float()
    max_depth = 10
    
    fov = 90
    lookfrom = Vector3(0,0,0)
    lookat = Vector3(0,0,-1)
    vup = Vector3(0,1,0)
    
    skyMode = 'sky'
    skyBox = None
    
    def render(self,world,screen):
        self.__initialize()
        ar = pxarray.PixelArray(screen)
        for j in range(self.screenHeight):
            for i in range(self.screenWidth):
                color = self.__pixColor(i, j, world)
                ar[i,j] = color
                #gfxdraw.pixel(screen, i, j, color)
            display.flip()
    def __initialize(self):
        self.pixels_samples_scale = 1/self.samples_per_pixel
        
        self.center = self.lookfrom
        
        focal_length = 1
        theta = degrees_to_radians(self.fov)
        h = math.tan(theta/2)
        self.viewHeight = 2*h*focal_length
        
        w = Vector3.normalize(self.lookfrom - self.lookat)
        u = Vector3.normalize(Vector3.cross(self.vup, w))
        v = Vector3.cross(w,u)
    
    def __get_ray(self,i,j):
        offset = self.__sample_square()
        pixel_sample = Vector3(i+offset.x - self.screenWidth/2, -(j+offset.x-self.screenHeight/2),-1)
        #pixel_sample.x /= self.screenHeight
        #pixel_sample.y /= self.screenHeight
        # pixel_sample = Vector3( (i+offset.x-self.screenWidth/2)/self.screenHeight,-(j+offset.x-self.screenHeight/2)/self.screenHeight, -1)
        pixel_sample.x *= self.viewHeight/self.screenHeight
        pixel_sample.y *= self.viewHeight/self.screenHeight

        ray_origin = self.center
        ray_direction = pixel_sample
        return(ray(ray_origin,ray_direction))
    
    def __sample_square(self):
        return(Vector3(random()-0.5, random()-0.5, 0))
    
    def __pixColor(self,i,j,world):
        color_vec = Vector3(0,0,0)
        for sample in range(self.samples_per_pixel):
            r = self.__get_ray(i,j)
            color_vec += self.__ray_color_vec(r, self.max_depth, world)
        color_vec = round(self.pixels_samples_scale * color_vec * 255)
        
        intensity = interval(0,255)
        color_vec.x = intensity.clamp(color_vec.x)
        color_vec.y = intensity.clamp(color_vec.y)
        color_vec.z = intensity.clamp(color_vec.z)
        
        color = Color(color_vec)
        return color.correct_gamma(1/2)

    def __ray_color_vec(self,r,depth,world):
        if(depth <= 0):
            return Vector3(0,0,0)
        
        rec = hit_record()
        if(world.hit(r,interval(EPSILON,infinity),rec)):
            #direction = rec.normal + random_unit_vector()
            #return 0.5 * self.__ray_color_vec(ray(rec.p,direction), depth-1, world)
            scattered = ray()
            attenuation = Vector3(0,0,0)
            if(rec.mat.scatter(r, rec, attenuation, scattered)):
                result = self.__ray_color_vec(scattered, depth-1, world)
                emittedLight = rec.mat.emissionColor * rec.mat.emissionStrength
                result.x = result.x * attenuation.x + emittedLight.x
                result.y = result.y * attenuation.y + emittedLight.y
                result.z = result.z * attenuation.z + emittedLight.z
                return result
            return Vector3(0,0,0)
        
        return self.__get_sky_color(r.direction)
    
    def __get_sky_color(self,dir):
        if(self.skyMode == 'sky'):
            unit_direction = Vector3.normalize(dir)
            a = 0.5*(unit_direction.y + 1)
            return Vector3(1,1,1).lerp(Vector3(.5,.7,1),a)
        if(self.skyMode == 'black'):
            return Vector3(0,0,0)
        unit_direction = Vector3.normalize(dir)
        u = 0.5 + math.atan2(unit_direction.z, unit_direction.x)/(2*pi)
        v = 0.5 + math.asin(-unit_direction.y)/pi
        skyBoxSize = self.skyBox.get_size()
        indexX = math.floor(u*skyBoxSize[0])
        indexY = math.floor(v*skyBoxSize[1])
        color = self.skyBox.get_at((indexX,indexY))
        gammaCorrected = Vector3(Color.correct_gamma(color,2)[0:3])
        return gammaCorrected / 255
        
    
