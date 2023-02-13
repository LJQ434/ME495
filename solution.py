#%%
import os
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants as c

class SOLUTION:

    def __init__(self,nextAvailableID):
        
        self.bodynumber = 3 + numpy.random.randint(6,size=1)[0]                             # number of bodies (initial with a number, randomly changed later)
        self.bodysize = 0.2+ 0.8*numpy.random.rand(3, self.bodynumber)                      # give rondom size to each direction of the body (0.2-1), xyz are all random 
        self.sensorstatus = numpy.random.randint(2,size = self.bodynumber)                  # decide whether add sensor to each body link
        self.sensornumber = sum(self.sensorstatus)
        while (self.sensornumber == 0):
            self.sensorstatus = numpy.random.randint(2,size = self.bodynumber)              # make sure at least have 1 sensor
            self.sensornumber = sum(self.sensorstatus)
        print(self.sensorstatus)
        self.motorstatus = numpy.random.randint(2,size = self.bodynumber-1) 
        self.motornumber = self.bodynumber - 1 ##### all joint has a motor

        self.weights = 2 * numpy.random.rand(self.sensornumber,self.motornumber) - 1        # weight of synapses
        
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
        pyrosim.Send_Cube(name="Box", pos=[8,8,0.25] , size=[0.5,0.5,0.5], mass=100000) #give a box in world (will not interact with snake)
        
        pyrosim.End()
        

    def Generate_Body(self,ID):
        
        ###############################################################
        ### torso 

        pyrosim.Start_URDF("body"+str(ID)+".urdf")  
        if self.sensorstatus[0] == 1:  colorifsensor='Green'
        else: colorifsensor='Cyan'
        pyrosim.Send_Cube(name="link0", 
                          pos=[0,0,0.5], 
                          size=[self.bodysize[0][0],self.bodysize[1][0],self.bodysize[2][0]],
                          color= colorifsensor
                          ) #link0, torso (first random body, bodyid=0)

        ### first link (on y+ direation )
        pyrosim.Send_Joint(name = "link0_link1" , parent= "link0" , child = "link1" , type = "revolute", position = [0, self.bodysize[1][0]/2 ,0.5], jointAxis = "1 0 0") #joint0-1 
        
        if self.sensorstatus[1] == 1:  colorifsensor='Green'
        else: colorifsensor='Cyan'
        pyrosim.Send_Cube(name= "link1",
                          pos=[0,self.bodysize[1][1]/2,0] ,
                          size=[self.bodysize[0][1],self.bodysize[1][1],self.bodysize[2][1]],
                          color = colorifsensor
                          ) #link1 (second random body, bodyid=1)

        ### linear snake body
        for linkid in range (2,self.bodynumber):
            pyrosim.Send_Joint(name = "link"+str(linkid-1)+"_link"+str(linkid) , parent= "link"+str(linkid-1) , child = "link"+str(linkid) , type = "revolute", position = [0,self.bodysize[1][linkid-1],0], jointAxis = "1 0 0") #new joint 
            if self.sensorstatus[linkid] == 1:  colorifsensor='Green'
            else: colorifsensor='Cyan'
            pyrosim.Send_Cube(name= "link"+str(linkid), 
                              pos=[0,self.bodysize[1][linkid]/2,0] , 
                              size=[self.bodysize[0][linkid],self.bodysize[1][linkid],self.bodysize[2][linkid]],
                              color = colorifsensor
                              ) #new link
        pyrosim.End()


    def Generate_Brain(self,ID):
        flag = 0
        #generate neurons
        pyrosim.Start_NeuralNetwork("brain"+str(ID)+".nndf")

        ###############################################################
        ### sensor neurons (on links)
        for linkid in range (self.bodynumber):
            if self.sensorstatus[linkid]==1:
                pyrosim.Send_Sensor_Neuron(name = flag , linkName = "link"+str(linkid))
                flag=flag+1

        ###############################################################
        ### mortor neurons (on joints)
        for linkid in range (self.motornumber):
            pyrosim.Send_Motor_Neuron( name = self.sensornumber + linkid , jointName = "link"+str(linkid)+"_link"+str(linkid+1))
            
        #generate synapses
        for currentRow in range(self.sensornumber): #name of sensor neurons
            for currentColumn in range(self.motornumber): #name of motor neurons
                pyrosim.Send_Synapse( sourceNeuronName = currentRow ,
                 targetNeuronName = currentColumn + c.numMotorNeurons , 
                 weight = self.weights[currentRow][currentColumn] )
 
        pyrosim.End()

    
    #############################################################################
    #  Mutation 
    #############################################################################
    def Mutate(self):
         
        ### mutation of body size
        randomRow = numpy.random.randint(0,self.bodynumber)
        for i in range (3):
            self.bodysize[i,randomRow]= 0.2+ 0.8*numpy.random.random()

        ### mutation of sensor distribution
        randomRow = numpy.random.randint(0,self.bodynumber)
        self.sensorstatus[randomRow] = int(numpy.random.randint(1,size=1))
        self.sensornumber = sum(self.sensorstatus)
        if self.sensornumber == 0:
            self.sensorstatus[randomRow] = 1
            self.sensornumber = sum(self.sensorstatus)

        ### mutation of synaesis weight
        randomRow = numpy.random.randint(0,self.sensornumber)
        randomColumn = numpy.random.randint(0,self.motornumber)
        self.weights[randomRow,randomColumn] = 2 * numpy.random.random() - 1
# %%
