import pygame
from pygame.color import THECOLORS
import pdb
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions as draw
from pymunk.pygame_util import from_pygame, to_pygame
import pymunk.util as u
import random
import math
import numpy as np
from MakeItLearn import *
import sys

width = 600 # Width Of The Game Window
height = 600  # Height Of The Game Window
pygame.init() 
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock() # Game Clock
SummarySensorData = []
StepSizeValue = 1/10 # Step Size For Simulation
ClockTickValue = 25  # Clock Tick
BotSpeed = 50 # Speed Of The Bot
model = Net(InputSize, NumClasses)
model.load_state_dict(torch.load('./SavedNets/NNBot.pkl'))
BotStartLocation =  2
if(len(sys.argv) >  1 and sys.argv[1] == "2"):
    BotStartLocation =  3
elif(len(sys.argv) >  1  and sys.argv[1] == "3"):
    BotStartLocation =  1    
elif(len(sys.argv) >  1  and sys.argv[1] == "4"):
    BotStartLocation =  4
    
def PointsFromAngle(angle):
    ### Returns The Unit Direction Vector With Given Angle ###
    return math.cos(angle),math.sin(angle)

def AngleBetweenAndSide(vector1, vector2):
    ### Returns The Angle Between Vectors And The Side Of Resultant Vector ###
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    side = 1 if(np.dot(vector1, vector2) < 0) else -1
    return side,np.arccos(np.clip(np.dot(vector1, vector2), -1.0, 1.0))
    
class BotEnv:    
    def __init__(self):
        ### Initializing Environment Variables ###
        global BotStartLocation
        self.crashed = False
        self.DetectCrash = 0
        self.space = pymunk.Space()
        if(BotStartLocation == 1):
            self.BuildBot(100, 100, 20)
        elif(BotStartLocation == 2):
            self.BuildBot(100, 300, 20)    
        elif(BotStartLocation == 3):
            self.BuildBot(100, 450, 20)
        elif(BotStartLocation == 4):
            self.BuildBot(500, 50, 20)
        self.num_steps = 0
        self.walls = []
        self.WallShapes = []
        self.WallRects = []
        WallBody, WallShape, WallRect = self.BuildWall(200, 50, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(200, 125, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(200, 550, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(200, 450, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(400, 350, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(400, 250, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(500, 250, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(600, 250, 50)
        self.WallRects.append(WallRect)
        WallBody, WallShape, WallRect = self.BuildWall(115, 950, 400)
        self.WallRects.append(WallRect)
        
    def BuildWall(self, x, y, r):
        ### Build Wall On The Map ###
        size = r
        WallRect = pygame.Rect(x-r,600-y-r, 2*r, 2*r)
        return WallRect,WallRect,WallRect

    def BuildBot(self, x, y, r):
        ### Build The Bot Object ###
        size = r
        BoxPoints = list(map(Vec2d, [(-size, -size), (-size, size), (size,size), (size, -size)]))
        mass  = 0.5
        moment = pymunk.moment_for_poly(mass,BoxPoints, Vec2d(0,0))
        self.Bot = pymunk.Body(mass, moment)
        self.Bot.position = Vec2d(x,y)
        self.Bot.angle = 1.54
        BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
        self.space.add(self.Bot)
        self.BotRect = pygame.Rect(x-r,600-y-r, 2*r, 2*r)
        return self.Bot
    
    def DrawEverything(self,flag=0):
        ### Write Everything On The Game Window ###
        img = pygame.image.load("./assets/intel.jpg")
        x, y = 580,550
        AdjustedImagePosition = (x-50,y+50)
        screen.blit(img,to_pygame(AdjustedImagePosition,screen))

        if(flag==0 and self.DetectCrash == 0):
            (self.BotRect.x,self.BotRect.y) = self.Bot.position[0],600-self.Bot.position[1]
            self.CircleRect = pygame.draw.circle(screen, (169,169,169), (self.BotRect.x,self.BotRect.y), 20, 0)
        ## If Collision Detected Draw Green
        elif(flag==0 and self.DetectCrash >= 1):
            (self.BotRect.x,self.BotRect.y) = self.Bot.position[0],600-self.Bot.position[1]
            self.CircleRect = pygame.draw.circle(screen, (0,255,0), (self.BotRect.x,self.BotRect.y), 20, 0)
        ## If Collision Detected Draw Red
        else:
            (self.BotRect.x,self.BotRect.y) = self.Bot.position[0],600-self.Bot.position[1]
            self.CircleRect = pygame.draw.circle(screen, (255,0,0), (self.BotRect.x,self.BotRect.y), 20, 0)
        img = pygame.image.load("./assets/spherelight.png")
        offset = Vec2d(img.get_size()) / 2.
        x, y =  self.Bot.position
        y = 600.0 -y
        AdjustedImagePosition = (x,y) - offset
        screen.blit(img,AdjustedImagePosition)
        for ob in self.WallRects:
            pygame.draw.rect(screen, (169,169, 169), ob)
    
    def PlanAngle(self,A,B):
        ### Find The Angle Between Two Vector ###
        angle = np.arctan2(B[1] - A[1], B[0] - A[0])
        return angle
        
    def _step(self, action, CrashStep=0):
        ### Take The Simulation One Step Further ###
        self.Bot.angle = self.Bot.angle % 6.2831853072
        ## If Action Is Left
        if action == 3:  
            self.Bot.angle -= 0.1
            self.PreviousBodyAngle =  self.Bot.angle
            self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
            BotDirection = self.BotDirection
            self.Bot.velocity = BotSpeed/2 * BotDirection
        ## If Action Is Right
        elif action == 4:
            self.Bot.angle += 0.1
            self.PreviousBodyAngle =  self.Bot.angle
            self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
            BotDirection = self.BotDirection
            self.Bot.velocity = BotSpeed * BotDirection
            self.Bot.velocity = BotSpeed/2 * BotDirection
        ## If Action Is Straight
        elif action == 5:
            PlannedAngle = self.PlanAngle(self.Bot.position,(600,600))
            move_sign = 0
            x1,y1 = PointsFromAngle(self.Bot.angle)
            x2,y2 = PointsFromAngle(PlannedAngle)
            side,between_angle = AngleBetweenAndSide((x1,y1),(x2,y2))
            ## Move Towards Destination - Calculate Resultant Vector Between Car And Goal.
            if(between_angle > 0.15):
                d = np.cross((x1,y1),(x2,y2))
                if(d > 0):
                        self.Bot.angle += 0.1
                        self.PreviousBodyAngle =  self.Bot.angle
                        self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
                        BotDirection = self.BotDirection
                        self.Bot.velocity = BotSpeed* BotDirection
                else:
                        self.Bot.angle -= 0.1
                        self.PreviousBodyAngle =  self.Bot.angle
                        self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
                        BotDirection = self.BotDirection
                        self.Bot.velocity = BotSpeed * BotDirection
            else:
                self.Bot.angle = PlannedAngle
                self.PreviousBodyAngle =  self.Bot.angle
                self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
                BotDirection = self.BotDirection
                self.Bot.velocity = BotSpeed * BotDirection
        screen.fill(THECOLORS["white"]) ## Clear The Screen
        self.DrawEverything()          ## Write Everything To The Game
        self.space.step(StepSizeValue)## Take One Step In Simulation
        clock.tick(ClockTickValue)    ## Tick The Clock
        ## Get The Current Location And The Sensors Data At Given Point.
        x, y = self.Bot.position        ## Get The Bot Position
        SensorsData = self.AllSensorSensorsData(x, y, self.Bot.angle) ## Get All The Sensor Data
        NormalizedSensorsData = [(x-100.0)/100.0 for x in SensorsData] ## Normalize The Sensor Values
        state = np.array([NormalizedSensorsData])
        SensorsData = np.append(SensorsData,math.degrees(self.Bot.angle))
        SensorsData = np.append(SensorsData,[0])
        print(SensorsData[:-2])  ## Print The Sensor Data
        DataTensor = torch.Tensor(SensorsData[:-1]).view(1,-1)
        if (model != None):
            ## Get Decision From Neural Network If There Is A Collison
            self.DetectCrash = model(Variable(DataTensor))
            self.DetectCrash = abs(np.round(self.DetectCrash.data[0][0]))
            if(self.DetectCrash > 0):
                SignalData = SensorsData[:-2]
                if(sum(SignalData[:2]) > sum(SignalData[-2:])):
                 self.DetectCrash = 3
                else:
                 self.DetectCrash = 4
        for ob in self.WallRects:
            if ob.colliderect(self.CircleRect):
                    self.crashed = True
                    self.RecoverFromCrash(BotDirection)
        if (x >= 580 or x <= 20 or y <= 20 or y >=680):
                    self.crashed = True
                    self.RecoverFromCrash(BotDirection)
        SignalData = SensorsData[:-2]
        return

    def RecoverFromCrash(self, BotDirection):
        ### Execute Following When Bot Crashes ###
        while self.crashed:
            self.crashed = False 
            for i in range(1):
                self.Bot.angle += 2
                self.BotDirection = Vec2d(PointsFromAngle(self.Bot.angle))
                BotDirection = self.BotDirection
                self.Bot.velocity = BotSpeed * BotDirection
                screen.fill(THECOLORS["white"])
                self.DrawEverything(flag=1)
                self.space.step(StepSizeValue)
                pygame.display.flip()
                clock.tick(ClockTickValue)
                
    def AllSensorSensorsData(self, x, y, angle):
        ### Return The All Sensor Values ###
        SensorsData = []
        MiddleSensorStartPoint = (25 + x, y)
        MiddleSensorEndPoint = (65 + x , y)
        NumberOfSensors = 5
        RelativeAngles = []
        AngleToBeginWith = 1.3
        OffsetIncrement =  (AngleToBeginWith*2)/(NumberOfSensors-1)
        RelativeAngles.append(-AngleToBeginWith)
        ## Generate Sensors
        for i in range(NumberOfSensors-1):
            RelativeAngles.append(RelativeAngles[i]+OffsetIncrement)
        SensorList = []
        ## Collect The Sensor Value From All Sensors
        for i in range(NumberOfSensors):
            SensorList.append([MiddleSensorStartPoint,MiddleSensorEndPoint, RelativeAngles[i]])
            SensorsData.append(self.SensorReading(SensorList[i], x, y, angle))
        pygame.display.update()
        return SensorsData

    def SensorReading(self, sensor, x, y, angle):
        ### Returns The Reading For A Single Sensor ###
        distance = 0
        (x1,y1) = sensor[0][0],sensor[0][1]
        (x2,y2) = sensor[1][0],sensor[1][1]
        SensorAngle = sensor[2]
        PixelsInPath = []
        NumberOfPoints = 100
        ## Generate Sensor Points
        for k in range(NumberOfPoints):
            x_new = x1 + (x2-x1) * (k/NumberOfPoints)
            y_new = y1 + (y2-y1) * (k/NumberOfPoints)
            PixelsInPath.append((x_new,y_new))
        for pixel in PixelsInPath:
            distance += 1
            PixelInGame = self.Rotate((x, y), (pixel[0], pixel[1]), angle + SensorAngle)
            SensorStartInGame = self.Rotate((x, y), (x1, PixelsInPath[-1][1]), angle + SensorAngle)
            SensorEndInGame = self.Rotate((x, y),  PixelsInPath[-1], angle + SensorAngle)
            if PixelInGame[0] <= 0 or PixelInGame[1] <= 0 or PixelInGame[0] >= width or PixelInGame[1] >= height:
                return distance
            else:
                for ob in self.WallRects:
                    if ob.collidepoint((PixelInGame[0],PixelInGame[1])): 
                        return distance
        ## Draw The Sensor
        pygame.draw.line(screen,(30,144,255),SensorStartInGame,SensorEndInGame)
        return distance
        
    def Rotate(self,origin, point, angle):
        ### Rotates A Point Along A Given Point ###
        x1, y1 = origin
        x2, y2 = point
        final_x = x1 + math.cos(angle) * (x2 - x1) - math.sin(angle) * (y2 - y1)
        final_y = y1 + math.sin(angle) * (x2 - x1) + math.cos(angle) * (y2 - y1)
        final_y = abs(width - final_y)
        return final_x,final_y

if __name__ == "__main__":
    env = BotEnv()
    random.seed(10)
    env._step(5)
    for i in range(2000):
        ## Check If Destination Is Reached
        if(env.Bot.position[0] > 500 and env.Bot.position[1] > 520):
            print("MISSION COMPLETE!")
            exit()
        ## Then Take Respective Action
        else:
            if (env.DetectCrash > 0):
                DrivingSide = env.DetectCrash
                for i in range(14):env._step(DrivingSide)
            else:
                x = 5
                env._step(x)

