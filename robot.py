#%%
import os
import numpy
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import sensor
import motor
import constants as c

class ROBOT:
    def __init__(self,physicsClient,solutionID):
        self.physicsClient=physicsClient
        self.RobotId = p.loadURDF("body"+solutionID+".urdf")
        self.motors = {}
        self.sensors = {}
        self.nn = NEURAL_NETWORK("brain"+solutionID+".nndf")
        

    ##############################################################################
    #  preparation
    ##############################################################################      
  
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
            #print(c.F[i])
            i=i+1

    ##############################################################################
    #  action
    ##############################################################################     

    def Sense(self,t):
       for linkName in pyrosim.linkNamesToIndices:
            #print(linkName)
            self.sensors[linkName].Get_Value(t)
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
        
    def Act(self,t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName1 = self.nn.Get_Motor_Neurons_Joint(neuronName)
                #print("!!!!!!motor neuron name:",neuronName)
                desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuronName)
                #print(neuronName)
                #print(jointName)
                #print(desiredAngle)
                pyrosim.Set_Motor_For_Joint(
                bodyIndex = self.RobotId,
                jointName = jointName1,
                controlMode = p.POSITION_CONTROL,
                targetPosition = desiredAngle, 
                maxForce = self.motors[jointName1].force)

        #for jointName in pyrosim.jointNamesToIndices:


    ##############################################################################
    #  evaluation
    ##############################################################################         

    def Get_Fitness(self,ID):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.RobotId)
        basePosition = basePositionAndOrientation[0]
        #Orientation = basePositionAndOrientation[1]
        self.xPosition = basePosition[0]
        self.yPosition = basePosition[1]
        self.zPosition = basePosition[2]
        fitness = (self.yPosition)*self.zPosition
        #print('x=',self.xCoordinateOfLinkZero)
        #print('y=',self.yCoordinateOfLinkZero)
        f = open("tmp"+ID+".txt","w")
        f.write(str(fitness) ) #distance it moves
        f.close()
        if os.path.isfile('fitness'+str(ID)+'.txt'):
            os.system("del fitness"+str(ID)+".txt") 
        os.rename("tmp"+str(ID)+".txt" , "fitness"+str(ID)+".txt")

    
# %%
