import gymnasium as gym
from gymnasium import spaces
import pygame, os, math, random
import numpy as np


class RaceTrackEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    cur_dir = os.getcwd()
    


    def __init__(self, render_mode=None, game_fps=60, rotation_amount=4, max_speed=7, acceleration_amount=0.3):
    
        self.game_fps = game_fps
        self.rotation_amount=rotation_amount
        self.max_speed=max_speed
        self.acceleration_amount=acceleration_amount
    
        self.screen2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = None
        def Generate_Random_Points(x, y, amount=12, offset=0): #THIS FUNCTION SHOULD BE PRETTIER, WHAT A FUCKING MESS. MAGIC WORKING ANYWAY, DONT TOUCH ANYMORE
            point_list = []
            factor = 24

            wall_points = amount // 4
            point_list.append([10+offset, random.randint(0+offset, y/factor+offset)])
            while wall_points > 0:
                if wall_points == 1:
                    point_list.append([x/wall_points-10-offset, random.randint(0+offset, y/factor+offset)])
                else:
                    point_list.append([x/wall_points-10+offset, random.randint(0+offset, y/factor+offset)])
                wall_points-=1

            wall_points = amount // 4
            point_list.append([10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
            while wall_points > 0:
                if wall_points == amount // 4:
                    point_list.append([x/wall_points-10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
                else:
                    point_list.append([x/wall_points-10-offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
                wall_points-=1
        
            wall_points = amount // 4
            point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), 10+offset])
            while wall_points > 0:
                if wall_points >= 2:
                    point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10+offset])
                else:
                    point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10-offset])
                wall_points-=1
        
            wall_points = amount - ((amount//4)*3)
            point_list.append([random.randint(0+offset, x/factor+offset), 10+offset])
            while wall_points > 0:
                if wall_points <= 1:
                    point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10-offset])
                else:
                    point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10+offset])
                wall_points-=1
        
            coords = np.array(point_list)
            cc_x, cc_y = coords.mean(0)
            x, y = coords.T
            angles = np.arctan2(x-cc_x, y-cc_y)
            indices = np.argsort(angles)
            return coords[indices]

        cur_dir = os.getcwd()
        self.observation_space = spaces.Box(low=-0.0, high=130.0, shape=(5,), dtype=np.float32)
        self.action_space = spaces.Discrete(4)
       
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        self.points = Generate_Random_Points(self.screen2.get_width(), self.screen2.get_height())
        self.points2 = Generate_Random_Points(self.screen2.get_width(), self.screen2.get_height(), offset=200)
        self.x = 100
        self.y = 100
        self.car_image = pygame.image.load(os.path.join(cur_dir, "img", "car_red.png"))
        self.car_rect = self.car_image.get_rect()
        self.car_rect.center=(self.x, self.y)
        self.car_rotation = 0
        self.car_direction = math.radians(self.car_rotation)
        self.car_speed = 0
        self.car_lidar = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.car_image_dir = {}
        self.car_rotated_image_rect = {}
        self.collision_lane = 50
        self.print_condition = 0
        self.collision_detect = 0
        i = 0
        while i <= 360:
            self.car_image_dir[i] = pygame.transform.rotate(self.car_image, i)
            self.car_rotated_image_rect[i] = self.car_image_dir[i].get_rect(center = self.car_rect.center)
            i+=1
        i = 0
        self.lines = []
        while i < len(self.points):
            try:
                self.lines.append((self.points[i], self.points[i+1]))
            except:
                self.lines.append((self.points[i], self.points[0]))
            i+=1
        i = 0
        self.lines2 = []
        while i < len(self.points2):
            try:
                self.lines2.append((self.points2[i], self.points2[i+1]))
            except:
                self.lines2.append((self.points2[i], self.points2[0]))
            i+=1
        self.window = None
        self.clock = None
        
    def _get_obs(self):
        return np.array([self.car_lidar[0], self.car_lidar[1], self.car_lidar[2], self.car_lidar[3], self.car_lidar[4]], dtype='f')
    
    def _get_info(self):
        return {"location" : self.car_rect.center}
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        def Generate_Random_Points(x, y, amount=12, offset=0): #THIS FUNCTION SHOULD BE PRETTIER, WHAT A FUCKING MESS. MAGIC WORKING ANYWAY, DONT TOUCH ANYMORE
            point_list = []
            factor = 24

            wall_points = amount // 4
            point_list.append([10+offset, random.randint(0+offset, y/factor+offset)])
            while wall_points > 0:
                if wall_points == 1:
                    point_list.append([x/wall_points-10-offset, random.randint(0+offset, y/factor+offset)])
                else:
                    point_list.append([x/wall_points-10+offset, random.randint(0+offset, y/factor+offset)])
                wall_points-=1

            wall_points = amount // 4
            point_list.append([10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
            while wall_points > 0:
                if wall_points == amount // 4:
                    point_list.append([x/wall_points-10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
                else:
                    point_list.append([x/wall_points-10-offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
                wall_points-=1
        
            wall_points = amount // 4
            point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), 10+offset])
            while wall_points > 0:
                if wall_points >= 2:
                    point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10+offset])
                else:
                    point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10-offset])
                wall_points-=1
        
            wall_points = amount - ((amount//4)*3)
            point_list.append([random.randint(0+offset, x/factor+offset), 10+offset])
            while wall_points > 0:
                if wall_points <= 1:
                    point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10-offset])
                else:
                    point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10+offset])
                wall_points-=1
        
            coords = np.array(point_list)
            cc_x, cc_y = coords.mean(0)
            x, y = coords.T
            angles = np.arctan2(x-cc_x, y-cc_y)
            indices = np.argsort(angles)
            return coords[indices]
        self.car_rect.center=(100,100)
        self.car_rotation = 0
        self.car_direction = math.radians(self.car_rotation)
        self.car_speed = 0
        self.points = Generate_Random_Points(self.screen2.get_width(), self.screen2.get_height())
        self.points2 = Generate_Random_Points(self.screen2.get_width(), self.screen2.get_height(), offset=200)
        
        self.lines = []
        i=0
        while i < len(self.points):
            try:
                self.lines.append((self.points[i], self.points[i+1]))
            except:
                self.lines.append((self.points[i], self.points[0]))
            i+=1
        i = 0
        self.lines2 = []
        while i < len(self.points2):
            try:
                self.lines2.append((self.points2[i], self.points2[i+1]))
            except:
                self.lines2.append((self.points2[i], self.points2[0]))
            i+=1
            
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def update(self, screen, i):
        self.rect.center=calculate_new_xy(self.rect.center,self.speed,self.direction, self.screen)
        self.rotated_image_rect[i] = self.image_dir[i].get_rect(center = self.rect.center)
        
    def step(self, action):
        if action == 0:
            self.car_rotation -= self.rotation_amount
            if self.car_rotation < 0:
                self.car_rotation = self.car_rotation + 360
            self.car_direction = math.radians(-self.car_rotation)
        if action == 1:
            self.car_speed += self.acceleration_amount
        if action == 2:
            self.car_rotation += self.rotation_amount
            if self.car_rotation > 360:
                self.car_rotation = self.car_rotation - 360
            self.car_direction = math.radians(-self.car_rotation)
        if action == 3:
            self.car_speed -= (self.acceleration_amount-0.1)
            
        self.print_condition += 1
        if self.print_condition == 120:
            print("ACTION_CHOOSE: %s" % action)
            self.print_condition = 0
            
        terminated = False
        if self.car_speed >= 0:
            reward = self.car_speed
        elif self.car_speed < 0:
            reward = -self.car_speed/2
        reward -= self.car_lidar[2]/65
        
        observation = self._get_obs()
        info = self._get_info()
        self.car_lidar = [0.0, 0.0, 0.0, 0.0, 0.0]
        if self.render_mode == "human":
            self._render_frame
            
        if self.car_speed > 0:
            self.car_speed-=0.1
        if self.car_speed < 0:
            self.car_speed+=0.1
            
        if self.car_speed > self.max_speed:
            self.car_speed -= (self.acceleration_amount + 0.2)
        elif self.car_speed < self.max_speed:
            self.car_speed += (self.acceleration_amount + 0.2)
            

        def calculate_new_xy(old_xy, speed, angle_in_radians, screen):
            new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
            new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
            return new_x, new_y
        self.car_rect.center=calculate_new_xy(self.car_rect.center,self.car_speed,self.car_direction, self.screen2)
        self.car_rotated_image_rect[self.car_rotation] = self.car_image_dir[self.car_rotation].get_rect(center = self.car_rect.center)
        
        self.x = self.car_rect.center[0] + math.cos(math.radians(self.car_rotation)) * self.collision_lane
        self.y = self.car_rect.center[1] + math.cos(math.radians(self.car_rotation)) * self.collision_lane
        
#TU POMIESZALEM
        startpoint = pygame.math.Vector2(self.car_rect.center)
        endpoint = pygame.math.Vector2(130, 0)
        
        i = -40
        j = 0
        
        def intersect_line_line(P0, P1, Q0, Q1):  
            d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
            if d == 0:
                return None
            t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
            u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
            if 0 <= t <= 1 and 0 <= u <= 1:
                return P1[0] * t + P0[0] * (1-t), P1[1] * t + P0[1] * (1-t)
            return None
            
        while i <= 40:
            final_endpoint = startpoint + endpoint.rotate((-self.car_rotation + i) % 360)
            i+=20
            for line in self.lines:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    self.car_lidar[j] = distance / 7
            for line in self.lines2:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    self.car_lidar[j] = distance / 7
            j+=1
        self.collision_detect = 0
        for line in self.lines:
            if self.car_rotated_image_rect[self.car_rotation].clipline(*line):
                self.collision_detect = 1
                if self.car_speed > 0:
                    self.car_speed = -self.car_speed/2 - 3
                elif self.car_speed < 0:
                    self.car_speed = -self.car_speed/2 + 3
                reward -= 10
                
        for line in self.lines2:
            if self.car_rotated_image_rect[self.car_rotation].clipline(*line):
                self.collision_detect = 1
                if self.car_speed > 0:
                    self.car_speed = -self.car_speed/2 - 3
                elif self.car_speed < 0:
                    self.car_speed = -self.car_speed/2 + 3
                reward -= 10
                
        if self.render_mode == "human":
            self._render_frame()
        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == "human":
            return self._render_frame()
        
    def _render_frame(self):
        
        if self.screen is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.font = pygame.font.SysFont("Arial" , 30 , bold = True)
            self.font_data = pygame.font.SysFont("Arial" , 20 , bold = False)
            pygame.display.set_caption('PatroCar')
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        self.screen.fill((64, 64, 64))
        
        startpoint = pygame.math.Vector2(self.car_rect.center)
        endpoint = pygame.math.Vector2(130, 0)
        
        i = -40
        j = 0
        
        def intersect_line_line(P0, P1, Q0, Q1):  
            d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
            if d == 0:
                return None
            t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
            u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
            if 0 <= t <= 1 and 0 <= u <= 1:
                return P1[0] * t + P0[0] * (1-t), P1[1] * t + P0[1] * (1-t)
            return None
        collision_string = self.font.render("Collision!" , 1, pygame.Color("RED"))
        while i <= 40:
            final_endpoint = startpoint + endpoint.rotate((-self.car_rotation + i) % 360)
            pygame.draw.line(self.screen, "white", startpoint, final_endpoint)
            i+=20
            for line in self.lines:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    pygame.draw.circle(self.screen, (255, 0, 0), intersection_point, 4)
                    self.car_lidar[j] = distance / 7
            for line in self.lines2:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    pygame.draw.circle(self.screen, (255, 0, 0), intersection_point, 4)
                    self.car_lidar[j] = distance / 7
            j+=1
            
        for line in self.lines:
            pygame.draw.line(self.screen, "white", *line)
                
        for line in self.lines2:
            pygame.draw.line(self.screen, "white", *line)
                
        #print(self.car_lidar)
                
        #self.car_image.convert_alpha()
        self.screen.blit(self.car_image_dir[self.car_rotation], self.car_rotated_image_rect[self.car_rotation])
        self.clock.tick(self.game_fps)
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render("FPS: %s" % fps , 1, pygame.Color("GREEN"))
        lidar_t = self.font_data.render("LIDAR: %s" % str(self.car_lidar) , 1, pygame.Color("RED"))
        speed_t = self.font_data.render("SPEED: %s" % str(round(self.car_speed, 2)) , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(self.screen.get_width()-150, 10))
        self.screen.blit(lidar_t,(20, self.screen.get_height()-60))
        self.screen.blit(speed_t,(20, self.screen.get_height()-40))
        if self.collision_detect == 1:
            self.screen.blit(collision_string,(self.screen.get_width()/2-100, self.screen.get_height()/2-20))
        
        pygame.event.pump()
        pygame.display.update()
        pygame.display.flip()
        

        if self.print_condition == 110:
            print("LIDAR: %s ###### SPEED: %s" % (self.car_lidar, self.car_speed))
        
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
        
# dupa = RaceTrackEnv(render_mode="human", game_fps=999, rotation_amount=1, max_speed=1, acceleration_amount=0.1)
# dupa._get_obs
# l=0
# while l < 500:
#     dupa.step(0)
#     dupa.step(1)
#     dupa._render_frame()
#     l+=1

