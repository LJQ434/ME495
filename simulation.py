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
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT()
        pyrosim.Prepare_To_Simulate(self.robot.RobotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()


    def RUN(self):
        for t in range (c.iter):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think(t)
            self.robot.Act(t)
            # step time
            time.sleep(0.01)
            self.robot.Save_Values()
    
    def __del__(self):
        p.disconnect()

# %%
