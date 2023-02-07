#%%
import pybullet_data
import pybullet as p
import numpy 
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import constants as c
import time

class SIMULATION:
    
    def __init__(self,directOrGUI,solutionID):
        if directOrGUI == "GUI": # means GUI
            self.physicsClient = p.connect(p.GUI)
        else: # means DIRECT
            self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD(self.physicsClient)
        self.robot = ROBOT(self.physicsClient,solutionID)
        pyrosim.Prepare_To_Simulate(self.robot.RobotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()


    def RUN(self,directOrGUI):
        for t in range (c.iter):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            # step time
            if directOrGUI == "GUI":
                time.sleep(0.00001)
            #self.robot.Save_Values()
   
            
    def Get_Fitness(self,ID):
        self.robot.Get_Fitness(ID)


    def __del__(self):
        p.disconnect()
        pass


# %%
