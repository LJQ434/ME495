#%%
import os
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants as c
from random import sample

class SOLUTION:

    def __init__(self,nextAvailableID):
        
        ### basic setting
        self.limbnumber = 2                                                                         # body = torso + 2*limb1(symetric) + 2*limb2(symetric)    # each limb is a 3D random snake
        self.maxlimbbodynumber = 5                                                            # maximium size to each limb  (set 4 for now)
        self.hiddenneuron = 8
        ### limb body number initialize
        self.number_of_limbbody = numpy.zeros(self.limbnumber, dtype = int)                  
        for i in range (self.limbnumber):
            self.number_of_limbbody[i] = numpy.random.randint(2,self.maxlimbbodynumber)            # body number of limb_i (random from 1 to maxlimbnumber)
        

        ### chromosomes decide body of each limb: two chromosome: array(limbnumber,3*maxlimbbodynumber) 
        self.chromosome_bodysize = 0.2 + 0.8*numpy.random.rand(self.limbnumber,self.maxlimbbodynumber,3)     # ex. size of limb_i body_j: (x,y,z) =  (self.chromosome_bodysize [i][3*j],self.chromosome_bodysize[i][3*j+1],self.chromosome_bodysize [i][3*j+2])
        #check body size(empty for now)
        
        self.chromosome_bodydirection = numpy.zeros((self.limbnumber,self.maxlimbbodynumber,3), dtype = int)     

        self.chromosome_bodydirection[0][0] = [1,1,0]  #first link of lamb 0 is fixed; limb 3 is symetric of limb 0
        self.chromosome_bodydirection[1][0] = [1,-1,0] #first link of lamb 1 is fixed; limb 4 is symetric of limb 1
        for limb in range (self.limbnumber):
            if self.number_of_limbbody[limb]>1:
                for body in range (1,self.maxlimbbodynumber):
                    self.chromosome_bodydirection[limb][body][0] =  numpy.random.randint(-1,1)        # ex. direction of limb_i body_j+1 to body_j: self.chromosome_bodydirection[i][3*j],[i][3*j+1],[i][3*j+2]
                    self.chromosome_bodydirection[limb][body][1] =  numpy.random.randint(-1,1)        # ex. (0,1,-1)= y positive + z negative direction
                    self.chromosome_bodydirection[limb][body][2] =  numpy.random.randint(-1,1)        # even no body is there, the direction information is still restored. just like gene
                    # check if all zero?
                    if sum(abs(self.chromosome_bodydirection[limb][body]))==0:  self.chromosome_bodydirection[limb][body][2] = -1
                    # check if at conor? (abs(xyz) =1)
                    if abs(self.chromosome_bodydirection[limb][body][0]*self.chromosome_bodydirection[limb][body][1]*self.chromosome_bodydirection[limb][body][2])==1:
                        self.chromosome_bodydirection[limb][body][2] = 0
                    # check if reverse back?
                    if sum(abs(self.chromosome_bodydirection[limb][body] + self.chromosome_bodydirection[limb][body-1])) ==0:
                        self.chromosome_bodydirection[limb][body] = self.chromosome_bodydirection[limb][body-1]
            

        ### chromosomes decide brain #(set the sensor number to be 2 for each limb, but not define where to put, but random set)
        self.sensornumber = 4
        self.chromosome_sonsor = numpy.zeros((2,self.maxlimbbodynumber), dtype = int )      # decide whether add sensor to each body link
        for limb in range (self.limbnumber):
            lst = list(range(0,self.number_of_limbbody[limb]))
            sensorbody = sample(lst,2)
            for i in range (2):
                 self.chromosome_sonsor [limb][sensorbody[i]] = 1
        self.sensornumber = 0
        for limb in range ( self.limbnumber):
            for body in range (self.number_of_limbbody[limb] ):
                self.sensornumber = self.sensornumber + self.chromosome_sonsor[limb][body]         # sensor number is sum within all existing limbs
        if  self.sensornumber != 4:
            print('!!!!!!sensor set wrong!!!!!!')
            print( self.chromosome_sonsor)
               
        ###
        self.weightslayer1 = 2 * (numpy.random.rand(self.sensornumber*2, self.hiddenneuron) -1)                        # weight of synapses (limb, 2 sensor, 8 hidden)
        self.weightslayer2 = 2 * (numpy.random.rand(self.hiddenneuron, 2* self.limbnumber, max(self.number_of_limbbody)) -1)              # weight of synapses (limb, 4 hidden, n motor)

        ### print check
        #print(self.totalsensornumber)
        #print(self.motornumber)
        #print(self.number_of_limbbody)
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
        self.record(ID)
        
        # run simulate
        os.system("start /B python simulate2.py "+ directOrGUI +" "+ str(ID) )

    def record(self,ID):
        f = open("sensorandmotor"+str(ID)+".txt","w")
        f.write(str(self.limbnumber))
        f.write(" ")
        f.write(str(self.sensornumber))
        f.write(" ")
        f.write(str(self.limbnumber))
        f.write(" ")
        
        

    def Only_simulate(self,directOrGUI,ID):
       
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
        ### print check
        #print(self.number_of_limbbody)

        ###############################################################
        ### torso 

        pyrosim.Start_URDF("body"+str(ID)+".urdf")  
        
        pyrosim.Send_Cube(name="Torso", 
                          pos=[0,0,3], 
                          size=[2,2,1],
                          color= 'Cyan'
                          ) #link0, torso (first random body, bodyid=0)
        

        ### limb loop
        for limb in range (self.limbnumber):
            
            ## first joint in the limb
            x = self.chromosome_bodydirection[limb][0][0]
            y = self.chromosome_bodydirection[limb][0][1]
            z = self.chromosome_bodydirection[limb][0][2]
            jx = abs(x)
            jy = abs(y)
            jz = abs(z)

            #print('for limb',limb,' the first link position (x,y,z) = ', x,y,z)

            pyrosim.Send_Joint(name = "Torso_limb" + str(limb) + "link0" ,
                               parent= "Torso" , child = "limb" + str(limb)+ "link0" , 
                               type = "revolute", position = (1*x, 1*y, 3 + 0.5*z),
                               jointAxis = str(jx)+" "+str(jy)+" "+str(jz)
                               ) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not finished here, haven't made random direction of it
            

            ## first body in the limb 
            sx = self.chromosome_bodysize[limb][0][0]
            sy = self.chromosome_bodysize[limb][0][1]
            sz = self.chromosome_bodysize[limb][0][2]
            if self.chromosome_sonsor[limb][0] == 1:  colorifsensor='Green'
            else: colorifsensor='Cyan'
            pyrosim.Send_Cube(name= "limb" + str(limb)+ "link0",
                          pos=[x*sx/2, y*sy/2, z*sz/2] ,
                          size=[sx,sy,sz],
                          color = colorifsensor
                          ) #link1 (second random body, bodyid=1)
            px = x*sx/2
            py = y*sy/2
            pz = z*sz/2


            ## if the limb has more than 1 body 
            if self.number_of_limbbody[limb]-1 > 0: 
                for body in range(1,self.number_of_limbbody[limb]):
                    # joint update
                    x = self.chromosome_bodydirection[limb][body][0]
                    y = self.chromosome_bodydirection[limb][body][1]
                    z = self.chromosome_bodydirection[limb][body][2]
                    jx = abs(x)
                    jy = abs(y)
                    jz = abs(z)
                    pyrosim.Send_Joint(name = "limb" + str(limb) + "link"+ str(body-1) + "_" + "limb" + str(limb) + "link"+ str(body),
                                       parent= "limb" + str(limb) + "link"+ str(body-1) ,
                                       child = "limb" + str(limb) + "link"+ str(body) , 
                                       type = "revolute", position = (px+sx/2*x, py+sy/2*y, pz+sz/2*z), 
                                       jointAxis = str(jx)+" "+str(jy)+" "+str(jz) 
                                       ) 
                    
                    # link update
                    sx = c.scaler**(body)*self.chromosome_bodysize[limb][body][0]
                    sy = c.scaler**(body)*self.chromosome_bodysize[limb][body][1]
                    sz = c.scaler**(body)*self.chromosome_bodysize[limb][body][2]
                    if self.chromosome_sonsor[limb][body] == 1:  colorifsensor='Green'
                    else: colorifsensor='Cyan'
                    pyrosim.Send_Cube(name= "limb" + str(limb) + "link"+ str(body),
                                pos=[x*sx/2, y*sy/2, z*sz/2],
                                size=[sx,sy,sz],
                                color = colorifsensor
                                ) #link1 (second random body, bodyid=1)
                    px = x*sx/2
                    py = y*sy/2
                    pz = z*sz/2


        ## symetirc limb
        for limb in range (self.limbnumber):
        
            ## first joint in the limb
            x = -self.chromosome_bodydirection[limb][0][0]
            y = self.chromosome_bodydirection[limb][0][1]
            z = self.chromosome_bodydirection[limb][0][2]
            jx = abs(x)
            jy = abs(y)
            jz = abs(z)

            #print('for limb',limb,'_sym the first link position (x,y,z) = ', x,y,z)

            pyrosim.Send_Joint(name = "Torso_limb" + str(limb+self.limbnumber) + "link0" ,
                            parent= "Torso" , child = "limb" + str(limb+self.limbnumber)+ "link0" , 
                            type = "revolute", position = (1*x, 1*y, 3 + 0.5*z),
                            jointAxis = str(jx)+" "+str(jy)+" "+str(jz)
                            ) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not finished here, haven't made random direction of it
            

            ## first body in the limb 
            sx = self.chromosome_bodysize[limb][0][0]
            sy = self.chromosome_bodysize[limb][0][1]
            sz = self.chromosome_bodysize[limb][0][2]
            if self.chromosome_sonsor[limb][0] == 1:  colorifsensor='Green'
            else: colorifsensor='Cyan'
            pyrosim.Send_Cube(name= "limb" + str(limb+self.limbnumber)+ "link0",
                        pos=[x*sx/2, y*sy/2, z*sz/2] ,
                        size=[sx,sy,sz],
                        color = colorifsensor
                        ) #link1 (second random body, bodyid=1)
            px = x*sx/2
            py = y*sy/2
            pz = z*sz/2


            ## if the limb has more than 1 body 
            if self.number_of_limbbody[limb]-1 > 0: 
                for body in range(1,self.number_of_limbbody[limb]):
                    # joint update
                    x = -self.chromosome_bodydirection[limb][body][0]
                    y = self.chromosome_bodydirection[limb][body][1]
                    z = self.chromosome_bodydirection[limb][body][2]
                    jx = abs(x)
                    jy = abs(y)
                    jz = abs(z)
                    pyrosim.Send_Joint(name = "limb" + str(limb+self.limbnumber) + "link"+ str(body-1) + "_" + "limb" + str(limb+self.limbnumber) + "link"+ str(body),
                                       parent= "limb" + str(limb+self.limbnumber) + "link"+ str(body-1) ,
                                       child = "limb" + str(limb+self.limbnumber) + "link"+ str(body) , 
                                       type = "revolute", position = (px+sx/2*x, py+sy/2*y, pz+sz/2*z), 
                                       jointAxis = str(jx)+" "+str(jy)+" "+str(jz) 
                                       ) 
                    
                    # link update
                    sx = c.scaler**(body)*self.chromosome_bodysize[limb][body][0]
                    sy = c.scaler**(body)*self.chromosome_bodysize[limb][body][1]
                    sz = c.scaler**(body)*self.chromosome_bodysize[limb][body][2]
                    if self.chromosome_sonsor[limb][body] == 1:  colorifsensor='Green'
                    else: colorifsensor='Cyan'
                    pyrosim.Send_Cube(name= "limb" + str(limb+self.limbnumber) + "link"+ str(body),
                                pos=[x*sx/2, y*sy/2, z*sz/2],
                                size=[sx,sy,sz],
                                color = colorifsensor
                                ) #link1 (second random body, bodyid=1)
                    px = x*sx/2
                    py = y*sy/2
                    pz = z*sz/2
        pyrosim.End()    
 

    def Generate_Brain(self,ID):
        
        #generate neurons
        pyrosim.Start_NeuralNetwork("brain"+str(ID)+".nndf")
        
        ##############################################################
        ### sensor neurons (on links)
        flag = 0
        for limb in range (self.limbnumber):
            for body in range(self.number_of_limbbody[limb]):
                if self.chromosome_sonsor[limb][body] == 1:
                    pyrosim.Send_Sensor_Neuron(name = flag , linkName = "limb" + str(limb) + "link"+ str(body))                    
                    flag=flag+1  
                    
        for limb in range (self.limbnumber):
            for body in range(self.number_of_limbbody[limb]):
                if self.chromosome_sonsor[limb][body] == 1:
                    pyrosim.Send_Sensor_Neuron(name = flag , linkName = "limb" + str(limb + self.limbnumber) + "link"+ str(body))  #sym
                    flag=flag+1

        sensorneuron = flag
        print(sensorneuron)

        ###############################################################
        ### hidden neurons (on joints)
        for i in range (self.hiddenneuron):
            pyrosim.Send_Hidden_Neuron(name = flag)
            flag = flag + 1
        

        # hiddenneuron = flag - sensorneuron

        ###############################################################
        ### mortor neurons (on joints)
        for limb in range (self.limbnumber):
            pyrosim.Send_Motor_Neuron( name = flag , jointName ="Torso_limb" + str(limb) + "link0") 
            flag=flag+1
            if self.number_of_limbbody[limb]>1:
                for body in range(1,self.number_of_limbbody[limb]):
                    pyrosim.Send_Motor_Neuron( name = flag , jointName ="limb" + str(limb) + "link"+ str(body-1) + "_" + "limb" + str(limb) + "link"+ str(body))  
                    flag=flag+1
        #sym            
        for limb in range (self.limbnumber):
            pyrosim.Send_Motor_Neuron( name = flag , jointName ="Torso_limb" + str(limb + self.limbnumber) + "link0") #sym
            flag=flag+1
            if self.number_of_limbbody[limb]>1:
                for body in range(1,self.number_of_limbbody[limb]):
                    pyrosim.Send_Motor_Neuron( name = flag , jointName = "limb" + str(limb + self.limbnumber) + "link"+ str(body-1) + "_" + "limb" + str(limb+self.limbnumber) + "link"+ str(body))  #sym
                    flag=flag+1
        

        ###############################################################    
        #generate synapses
        #layer1 (sensor to hidden)
        for limb in range (self.limbnumber):
            for currentRow in range(2): #name of sensor neurons
                for currentColumn in range(self.hiddenneuron): #name of hidden neurons
                    pyrosim.Send_Synapse( sourceNeuronName = currentRow,                # all sensor neuron connect to all hidden neurons
                    targetNeuronName = currentColumn + sensorneuron,
                    weight = self.weightslayer1[currentRow][currentColumn] )
                    
        #layer2 (hidden to motor)
        for currentRow in range(self.hiddenneuron): #name of hidden neurons
            for limb in range (self.limbnumber):
                for currentColumn in range(self.number_of_limbbody[limb]): #name of motor neurons
                    pyrosim.Send_Synapse( sourceNeuronName = currentRow + sensorneuron,
                    targetNeuronName = sensorneuron + self.hiddenneuron+ currentColumn + limb*self.number_of_limbbody[0],
                    weight = self.weightslayer2[currentRow][limb][currentColumn] )
                    #sym
                    pyrosim.Send_Synapse( sourceNeuronName = currentRow + sensorneuron,
                    targetNeuronName = sensorneuron + self.hiddenneuron+ currentColumn + limb*self.number_of_limbbody[0] + self.number_of_limbbody[0]+self.number_of_limbbody[1],
                    weight = self.weightslayer2[currentRow][limb+2][currentColumn] )


        pyrosim.End()


    
    #############################################################################
    #  Mutation 
    #############################################################################
    def Mutate(self,generation):
        
        ### shape mutate in every 20 generation:
        if generation % 10 == 0:
            #limb number change
            limb = numpy.random.randint(0,self.limbnumber) #choose a limb
            if self.number_of_limbbody[limb] == self.maxlimbbodynumber:
                self.number_of_limbbody[limb] =  self.number_of_limbbody[limb] - 1
            if self.number_of_limbbody[limb] == 2:
                self.number_of_limbbody[limb] =  self.number_of_limbbody[limb] + 1
            else:
                self.number_of_limbbody[limb] =  self.number_of_limbbody[limb] + int( 2*(numpy.random.randint(0,1)-0.5) ) # random +1 or -1 link
            
            # limb direction change
            limb = numpy.random.randint(0,self.limbnumber) #choose a limb
            body = numpy.random.randint(1,self.number_of_limbbody[limb])
            self.chromosome_bodydirection[limb][body][0] =  numpy.random.randint(-1,1)        # ex. direction of limb_i body_j+1 to body_j: self.chromosome_bodydirection[i][3*j],[i][3*j+1],[i][3*j+2]
            self.chromosome_bodydirection[limb][body][1] =  numpy.random.randint(-1,1)        # ex. (0,1,-1)= y positive + z negative direction
            self.chromosome_bodydirection[limb][body][2] =  numpy.random.randint(-1,1)        # even no body is there, the direction information is still restored. just like gene
            # check if reverse back?
            if sum(abs(self.chromosome_bodydirection[limb][body] + self.chromosome_bodydirection[limb][body-1])) ==0:
                self.chromosome_bodydirection[limb][body] = self.chromosome_bodydirection[limb][body-1]
            # check if all zero?
            if sum(abs(self.chromosome_bodydirection[limb][body]))==0:  self.chromosome_bodydirection[limb][body][2] = -1
            # check if at conor? (abs(xyz) =1)
            if abs(self.chromosome_bodydirection[limb][body][0]*self.chromosome_bodydirection[limb][body][1]*self.chromosome_bodydirection[limb][body][2])==1:
                self.chromosome_bodydirection[limb][body][2] = 0

            #regenerate weights
            self.weightslayer1 = 2 * (numpy.random.rand(self.sensornumber*2, self.hiddenneuron) -1)                        # weight of synapses (limb, 2 sensor, 8 hidden)
            self.weightslayer2 = 2 * (numpy.random.rand(self.hiddenneuron, 2* self.limbnumber, max(self.number_of_limbbody)) -1)              # weight of synapses (limb, 4 hidden, n motor)

        ### mutation of body size 
        limb =  numpy.random.randint(0,self.limbnumber)
        randomRow = numpy.random.randint(0,self.number_of_limbbody[limb])
        self.chromosome_bodysize[limb][randomRow]= 0.2+ 0.8*numpy.random.random()
        self.chromosome_bodysize[limb][randomRow]= 0.2+ 0.8*numpy.random.random()
        self.chromosome_bodysize[limb][randomRow]= 0.2+ 0.8*numpy.random.random()


        ### mutation of sensor distribution
        self.chromosome_sonsor = numpy.zeros((2,self.maxlimbbodynumber), dtype = int )     
        for limb in range (self.limbnumber):
            lst = list(range(0,self.number_of_limbbody[limb]))
            sensorbody = sample(lst,2)
            for i in range (2):
                 self.chromosome_sonsor [limb][sensorbody[i]] = 1
        self.sensornumber = 0
        for limb in range ( self.limbnumber):
            for body in range (self.number_of_limbbody[limb] ):
                self.sensornumber = self.sensornumber + self.chromosome_sonsor[limb][body]         # sensor number is sum within all existing limbs
        if  self.sensornumber != 4:
            print('!!!!!!sensor set wrong!!!!!!')
            print(self.sensornumber)
        
        ### mutation of synaesis weight
        randomRow = numpy.random.randint(0,self.sensornumber*2)
        randomColumn = numpy.random.randint(0,self.hiddenneuron)
        self.weightslayer1[randomRow][randomColumn] = 2 * numpy.random.random() - 1
        
        randlimb = numpy.random.randint(0,self.limbnumber)
        randomRow = numpy.random.randint(0,self.hiddenneuron)
        randomColumn = numpy.random.randint(0,self.number_of_limbbody[randlimb])
        self.weightslayer2[randomRow][limb+2*numpy.random.randint(0,2)][randomColumn] = 2 * numpy.random.random() - 1


       

# %%
