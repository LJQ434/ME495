#%%
import numpy
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import sensor
import motor
import constants as c

class ROBOT:
    def __init__(self):
        self.RobotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

    def Prepare_To_Sense(self):
        #self.sensors = sensor.SENSOR()
        for linkName in pyrosim.linkNamesToIndices:
            #print(linkName)
            self.sensors[linkName] = sensor.SENSOR(linkName)
    
    def Prepare_To_Act(self):
        i=0
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = motor.MOTOR(jointName)
            self.motors[jointName].Prepare_To_Act()
            self.motors[jointName].Set_Value(c.am[i],c.p[i],c.f[i],c.F[i])
            #print(c.am[i])
            i=i+1

    def Sense(self,t):
       for linkName in pyrosim.linkNamesToIndices:
            #print(linkName)
            self.sensors[linkName].Get_Value(t)

    def Act(self,t):
        for jointName in pyrosim.jointNamesToIndices:
            pyrosim.Set_Motor_For_Joint(
            bodyIndex = self.RobotId,
            jointName = jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motors[jointName].motorValues[t],
            maxForce = self.motors[jointName].force)
    
    def Save_Values(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName].Save_Values()

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Save_Values()

            #self.motors[jointName] = sensor.MOTOR(jointName)

# %%
