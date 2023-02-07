#%%
import os
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants as c

class SOLUTION:

    def __init__(self,nextAvailableID):

        self.weights = 2 * numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons) - 1
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
        assert os.path.isfile("fitness"+str(ID)+".txt")
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
        pyrosim.Send_Cube(name="Box", pos=[0,8,0.25] , size=[10,10,0.5], mass=100000)
        
        pyrosim.End()
        

    def Generate_Body(self,ID):
        
        ###############################################################
        ### torso 

        pyrosim.Start_URDF("body"+str(ID)+".urdf") 
        pyrosim.Send_Cube(name="Torso", pos=[0,0,2] , size=[0.4,0.8,0.4], mass=2) #link1
        
        ###############################################################
        ### first tentacle
    
        pyrosim.Send_Joint(name = "Torso_link11" , parent= "Torso" , child = "link11" , type = "revolute", position = [0,0.4,1.8], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link11", pos=[0,0,-0.5] , size=[0.5,0.5,1]) #link2
        pyrosim.Send_Joint(name = "link11_link12" , parent= "link11" , child = "link12" , type = "revolute", position =  [0,0,-1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link12", pos=[0,0,-0.3]  , size=[0.4,0.4,0.6]) #link2
        pyrosim.Send_Joint(name = "link12_link13" , parent= "link12" , child = "link13" , type = "revolute", position = [0,0,-0.6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link13", pos=[0,0.1,-0.1] , size=[0.4,0.6,0.2]) #link2

    
        pyrosim.Send_Joint(name = "Torso_link21" , parent= "Torso" , child = "link21" , type = "revolute", position =[0,-0.4,1.8], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link21", pos=[0,0,-0.5] , size=[0.5,0.5,1]) #link2
        pyrosim.Send_Joint(name = "link21_link22" , parent= "link21" , child = "link22" , type = "revolute", position =  [0,0,-1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link22", pos=[0,0,-0.3]  , size=[0.4,0.4,0.6]) #link2
        pyrosim.Send_Joint(name = "link22_link23" , parent= "link22" , child = "link23" , type = "revolute", position = [0,0,-0.6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="link23", pos=[0,0.1,-0.1] , size=[0.4,0.6,0.2]) #link2

        
        pyrosim.End()


    def Generate_Brain(self,ID):

        #generate neurons
        pyrosim.Start_NeuralNetwork("brain"+str(ID)+".nndf")
        
        ###############################################################
        ### sensor neurons (on links)
        
        #pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "link11")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "link12")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "link13")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "link21")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "link22")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "link23")

   

        ###############################################################
        ### mortor neurons (on joints)
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_link11")
        pyrosim.Send_Motor_Neuron( name = 7, jointName = "link11_link12")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "link12_link13")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_link21")
        pyrosim.Send_Motor_Neuron( name = 10, jointName = "link21_link22")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "link22_link23")

        
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
