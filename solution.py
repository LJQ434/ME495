#%%
import os
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants as c

class SOLUTION:

    def __init__(self,nextAvailableID):

        self.weights = 2 * numpy.random.rand(4,8) - 1
        self.myID = nextAvailableID
        self.fitness = 0
        
    #############################################################################
    #  start and end simulation 
    #############################################################################

    def Start_Simulation(self,directOrGUI,ID):
       
        # create world and robot
        self.Create_World()
        self.Generate_Body(ID)
        self.Generate_Brain(ID)
        
        # run simulate
        os.system("start /B python simulate2.py "+ directOrGUI +" "+ str(ID) )


    def Wait_For_Simulation_To_End(self,directOrGUI,ID):
        
        while not os.path.exists("fitness"+str(ID)+".txt"):
            time.sleep(0.01)
        
        # read fitness
        f = open("fitness"+str(ID)+".txt","r")
        self.fitness = float(f.read())
        f.close()

        #print("group",str(ID),"'s fitness is:",self.fitness) # print fitness

        os.system("del fitness"+str(ID)+".txt") 


    #############################################################################
    # generate world, body, brain
    #############################################################################
    def Create_World(self):

        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0,2,0.5] , size=[1,1,1])
        pyrosim.End()
        

    def Generate_Body(self,ID):
        
        ###############################################################
        ### torso 

        pyrosim.Start_URDF("body"+str(ID)+".urdf") 
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1]) #link1
        
        ###############################################################
        ### upper leg
        # leg 1: frontleg
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2 ,1, 0.2]) #link2
        # leg 2: backleg
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1] , jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2 ,1, 0.2]) #link3
        # leg 3: left leg
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0,1.0] , jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2]) #link4
        # leg 4: right leg
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1.0] , jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1,0.2,0.2]) #link5
        
        ###############################################################
        ### lower leg
        # leg 1: frontleg
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0" )
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2, 0.2, 1]) #link6
        # leg 2: backleg
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0" )
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2, 0.2, 1]) #link7
        # leg 3: left leg
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1,0,0], jointAxis ="0 1 0" )
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2, 0.2, 1]) #link8
        # leg 4: right leg
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1,0,0], jointAxis ="0 1 0" )
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2, 0.2, 1]) #link9

        
        pyrosim.End()


    def Generate_Brain(self,ID):

        #generate neurons
        pyrosim.Start_NeuralNetwork("brain"+str(ID)+".nndf")
        
        ###############################################################
        ### sensor neurons (on links)
        
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")

        ###############################################################
        ### mortor neurons (on joints)
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")
        
        
        #generate synapses
        for currentRow in range(c.numSensorNeurons): #name of sensor neurons
            for currentColumn in range(c.numMotorNeurons): #name of motor neurons
                pyrosim.Send_Synapse( sourceNeuronName = currentRow ,
                 targetNeuronName = currentColumn + c.numMotorNeurons , 
                 weight = self.weights[currentRow][currentColumn] )
    
        pyrosim.End()

    
    #############################################################################
    #  Mutation 
    #############################################################################
    def Mutate(self):
        randomRow = numpy.random.randint(1,c.numSensorNeurons)
        randomColumn = numpy.random.randint(1,c.numMotorNeurons)
        self.weights[randomRow,randomColumn] = 2 * numpy.random.random() - 1

# %%
