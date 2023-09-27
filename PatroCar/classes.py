import pygame, os, math
cur_dir = os.getcwd()

def calculate_new_xy(old_xy, speed, angle_in_radians, screen):
    new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
    #if new_x < 0 or new_x + 30 > screen.get_width():
    #    new_x = old_xy[0] - (speed*math.cos(angle_in_radians))
    #if new_y < 0 or new_y + 30 > screen.get_height():
    #    new_y = old_xy[1] - (speed*math.sin(angle_in_radians))
    return new_x, new_y

class Car:
    def __init__(self, image_name, screen, x=100, y=100, rotation=0, speed=0):
        self.screen = screen
        self.image = pygame.image.load(os.path.join(cur_dir, "img", image_name)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center=(x, y)
        self.rotation = rotation
        self.direction = math.radians(rotation)
        self.speed = speed
        self.lidar = [False, False, False, False, False]
        
        self.image_dir = {}
        self.rotated_image_rect = {}
        i = 0
        while i <= 360:
            self.image_dir[i] = pygame.transform.rotate(self.image, i)
            self.rotated_image_rect[i] = self.image_dir[i].get_rect(center = self.rect.center)
            i+=1
    
    def update(self, screen, i):
        self.rect.center=calculate_new_xy(self.rect.center,self.speed,self.direction, self.screen)
        self.rotated_image_rect[i] = self.image_dir[i].get_rect(center = self.rect.center)
        


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (124,252,0))

    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (124,252,0))
        display.blit(self.text, (display.get_width() - 70, 0))