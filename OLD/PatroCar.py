import pygame, os, math, random, sys
from classes import Car, cur_dir, FPS
from point_generator import Generate_Random_Points
from pygame.locals import *

#Init Simulation
pygame.init()
screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #FULLSCREEN
#screen = pygame.display.set_mode([screen_width, screen_height]) #WINDOW MODE
pygame.display.set_caption('PatroCar')
clock = pygame.time.Clock()  
fps_font = pygame.font.SysFont("Verdana", 20)

try:
    no_cars = int(sys.argv[1])
except:
    print("Podaj liczbę samochodów jako pierwszy argument")
    sys.exit()
    
print("Wybrano %s samochodów" % no_cars)

#CREATE CARS
car_colors_list = ["car_black.png", "car_blue.png", "car_green.png", "car_lavend.png", "car_pink.png", "car_violet.png", "car_white.png", "car_yellow.png"]
i = 0
cars_list = []
while i < no_cars:
    cars_list.append(Car(random.choice(car_colors_list), screen))
    i+=1
    
#CREATE POINTS FOR MAP
points = Generate_Random_Points(screen.get_width(), screen.get_height())
points2 = Generate_Random_Points(screen.get_width(), screen.get_height(), offset=200)


collision_lane = 50 #FORGOT WTF IS THIS, MAYBE NECCESARY

#FUNCTION CALCULATE INTERSECTION POINT BETWEEN LIDAR AND MAP
def intersect_line_line(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return P1[0] * t + P0[0] * (1-t), P1[1] * t + P0[1] * (1-t)
    return None

#CREATE LINES BETWEEN POINTS FOR MAP
i = 0
#lines = [((1, screen.get_height()-1), (1, 1)), ((screen.get_width()-1, 1), (1, 1)), ((screen.get_width()-1, screen.get_height()-1), (screen.get_width()-1, 1)), ((screen.get_width()-1, screen.get_height()-1), (1, screen.get_height()-1))]
lines = []
while i < len(points):
    try:
        lines.append((points[i], points[i+1]))
    except:
        lines.append((points[i], points[0]))
    #print(points[i])
    i+=1
i = 0
lines2 = []
while i < len(points2):
    try:
        lines2.append((points2[i], points2[i+1]))
    except:
        lines2.append((points2[i], points2[0]))
    #print(points2[i])
    i+=1

#INITIALIZE GAME CLOCK
fps = FPS()

#RED CAR FOR THE PLAYER, RED IS FASTEST!
car_red = Car("car_red.png", screen)
cars_list.append(car_red)

#LETS GO
running = True
while running:
    
    #IF BORED, QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #KEYS FOR PLAYER
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_red.rotation+=2
        if car_red.rotation >= 360:
            car_red.rotation = 0
        car_red.direction = math.radians(-car_red.rotation)
    if keys[pygame.K_RIGHT]:
        car_red.rotation-=2
        if car_red.rotation <= 0:
            car_red.rotation = 360
        car_red.direction = math.radians(-car_red.rotation)
    if keys[pygame.K_UP]:
        if car_red.speed <= 7:
            car_red.speed+=0.2
    if keys[pygame.K_DOWN]:
        if car_red.speed > -3:
            if car_red.speed > 0:
                car_red.speed-=0.4
            elif car_red.speed > -100:
                car_red.speed-=0.2
                
                
    #GIVE EVERY CAR RANDOM VALUES EVERY LOOP AND USE BUILT-IN LIDAR, REMOVE AFTER AI!
    for car in cars_list:
        if car != car_red:
            acceleration = random.randint(0, 10)
            turn = random.randint(0, 3)
            if acceleration == 0:
                if car.speed > -3:
                    if car.speed > 0:
                        car.speed-=0.4
                    elif car.speed > -100:
                        car.speed-=0.2
            if acceleration >= 2:
                if car.speed <= 7:
                    car.speed+=0.2

        #LIDAR LINES, FROM LEFT TO RIGHT - TO REMOVE
            if car.lidar[0] == True:
                car.rotation -=4
                if car.rotation <= 0:
                    car.rotation = 360 + car.rotation
                car.direction = math.radians(-car.rotation)
                car.lidar[0] = False
            if car.lidar[1] == True:
                car.rotation -=1
                if car.rotation <= 0:
                    car.rotation = 360 + car.rotation
                car.direction = math.radians(-car.rotation)
                car.lidar[1] = False
            if car.lidar[2] == True:
                car.rotation -=1
                if car.rotation <= 0:
                    car.rotation = 360 + car.rotation
                car.speed-=0.3
                car.lidar[2] = False
            if car.lidar[3] == True:
                car.rotation +=1
                if car.rotation > 360:
                    car.rotation = car.rotation - 360
                car.direction = math.radians(-car.rotation)
                car.lidar[3] = False
            if car.lidar[4] == True:
                car.rotation +=2
                if car.rotation > 360:
                    car.rotation = car.rotation - 360
                car.direction = math.radians(-car.rotation)
                car.lidar[4] = False
             
    #SOME BASIC PHYSICS (SLOW DOWN IF NOT ACCELERATING)
    for car in cars_list:
        if car.speed > 0:
            car.speed-=0.1
        if car.speed < 0:
            car.speed+=0.1

    #CARS PLACEMENT ON SCREEN
    screen.fill((64, 64, 64))
    for car in cars_list:
        car.update(screen, car.rotation)
        x = car.rect.center[0] + math.cos(math.radians(car.rotation)) * collision_lane
        y = car.rect.center[1] + math.cos(math.radians(car.rotation)) * collision_lane
        startpoint = pygame.math.Vector2(car.rect.center)
        endpoint = pygame.math.Vector2(130, 0)
        
        i = -40
        j = 0
        
        #LIDAR
        while i <= 40:
            final_endpoint = startpoint + endpoint.rotate((-car.rotation + i) % 360)
            pygame.draw.line(screen, "white", startpoint, final_endpoint)
            i+=20
            for line in lines:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    print("Lidar %s - %s jednostek " % (j, distance))
                    pygame.draw.circle(screen, (255, 0, 0), intersection_point, 4)
                    car.lidar[j] = True
            for line in lines2:
                intersection_point = intersect_line_line(startpoint, final_endpoint, line[0], line[1])
                if intersection_point != None:
                    distance = math.dist(intersection_point, startpoint)
                    print("Lidar %s - %s jednostek " % (j, distance))
                    pygame.draw.circle(screen, (255, 0, 0), intersection_point, 4)
                    car.lidar[j] = True
            j+=1
            #print(car.lidar)
    
    #COLLISION DETECTION WITH MAP
    for line in lines:
        pygame.draw.line(screen, "white", *line)
        for car in cars_list:
            if car.rotated_image_rect[car.rotation].clipline(*line):
                car.speed = -car.speed
        
    for line in lines2:
        pygame.draw.line(screen, "white", *line)
        for car in cars_list:
            if car.rotated_image_rect[car.rotation].clipline(*line):
                car.speed = -car.speed
        
    
    #FINALLY DRAW CARS
    for car in cars_list:
        screen.blit(car.image_dir[car.rotation], car.rotated_image_rect[car.rotation])
    
    #DRAW FPS CLOCK
    fps.render(screen)
    #UPDATE GAME SCREEN
    pygame.display.flip()
    fps.clock.tick(60)
    
pygame.quit()