#%%
import os
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants as c

class SOLUTION:

    def __init__(self,nextAvailableID):
        
        ### basic setting
        self.limbnumber = 2                                                                         # body = torso + 2*limb1(symetric) + 2*limb2(symetric)    # each limb is a 3D random snake
        self.maxlimbbodynumber = 4                                                                  # maximium size to each limb  (set 4 for now)

        ### limb body number initialize
        self.number_of_limbbody = numpy.zeros(self.limbnumber, dtype = int)                  
        for i in range (self.limbnumber):
            self.number_of_limbbody[i] = numpy.random.randint(1,self.maxlimbbodynumber)            # body number of limb_i (random from 1 to maxlimbnumber)
        

        ### chromosomes decide body of each limb: two chromosome: array(limbnumber,3*maxlimbbodynumber) 
        self.chromosome_bodysize = 0.2 + 0.8*numpy.random.rand(self.limbnumber,3*self.maxlimbbodynumber)     # ex. size of limb_i body_j: (x,y,z) =  (self.chromosome_bodysize [i][3*j],self.chromosome_bodysize[i][3*j+1],self.chromosome_bodysize [i][3*j+2])
        self.chromosome_bodydirection = numpy.zeros((self.limbnumber,3*self.maxlimbbodynumber), dtype = int)     
        flag =1
        while (flag == 1):
            for limb in range ( self.limbnumber):
                for body in range (self.maxlimbbodynumber):
                    self.chromosome_bodydirection[limb][3*body]   =  numpy.random.randint(-1,1)        # ex. direction of limb_i body_j+1 to body_j: self.chromosome_bodydirection[i][3*j],[i][3*j+1],[i][3*j+2]
                    self.chromosome_bodydirection[limb][3*body+1] =  numpy.random.randint(-1,1)        # ex. (0,1,-1)= y positive + z negative direction
                    self.chromosome_bodydirection[limb][3*body+2] =  numpy.random.randint(-1,1)        # even no body is there, the direction information is still restored. just like gene
                    if sum(self.chromosome_bodydirection[limb])==0:  self.chromosome_bodydirection[limb][3*body] = 1
                self.chromosome_bodydirection[limb][0] = 1
            if sum(abs(self.chromosome_bodydirection[0] - self.chromosome_bodydirection[1])) == 0: flag =1
            else: flag =0
            
            

        ### chromosomes decide brain
        self.sensornumber =0
        self.chromosome_sonsor = numpy.random.randint(2, size = (2,self.maxlimbbodynumber) )       # decide whether add sensor to each body link
        for limb in range ( self.limbnumber):
            for body in range (self.number_of_limbbody[limb] ):
                self.sensornumber = self.sensornumber + self.chromosome_sonsor[limb][body]         # sensor number is sum within all existing limbs

        self.totalsensornumber = self.sensornumber * 2                                             # *2 becasue symetric 
        self.totalmotornumber =  sum(self.number_of_limbbody)  *2                                  # motor on every joint  # *2 becasue symetric 
        self.weights = 2 * numpy.random.rand(self.totalsensornumber,self.totalmotornumber)         # weight of synapses
        
        ### print check
        #print(self.totalsensornumber)
        #print(self.totalmotornumber)
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
        print(self.number_of_limbbody)

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
            x = 1
            y = self.chromosome_bodydirection[limb][1]
            z = self.chromosome_bodydirection[limb][2]
            jx = abs(x)
            jy = abs(y)
            jz = abs(z)

            print('for limb',limb,' the first link position (x,y,z) = ', x,y,z)

            pyrosim.Send_Joint(name = "Torso_limb" + str(limb) + "link0" ,
                               parent= "Torso" , child = "limb" + str(limb)+ "link0" , 
                               type = "revolute", position = (1*x, 1*y, 3 + 0.5*z),
                               jointAxis = str(jx)+" "+str(jy)+" "+str(jz)
                               ) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not finished here, haven't made random direction of it
            

            ## first body in the limb 
            sx = self.chromosome_bodysize[limb][0]
            sy = self.chromosome_bodysize[limb][1]
            sz = self.chromosome_bodysize[limb][2]
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
                    x = self.chromosome_bodydirection[limb][3*body]
                    y = self.chromosome_bodydirection[limb][3*body+1]
                    z = self.chromosome_bodydirection[limb][3*body+2]
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
                    sx = c.scaler**(body)*self.chromosome_bodysize[limb][3*body]
                    sy = c.scaler**(body)*self.chromosome_bodysize[limb][3*body+1]
                    sz = c.scaler**(body)*self.chromosome_bodysize[limb][3*body+2]
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
            x = -1
            y = self.chromosome_bodydirection[limb][1]
            z = self.chromosome_bodydirection[limb][2]
            jx = abs(x)
            jy = abs(y)
            jz = abs(z)

            print('for limb',limb,'_sym the first link position (x,y,z) = ', x,y,z)

            pyrosim.Send_Joint(name = "Torso_limb" + str(limb+self.limbnumber) + "link0" ,
                            parent= "Torso" , child = "limb" + str(limb+self.limbnumber)+ "link0" , 
                            type = "revolute", position = (1*x, 1*y, 3 + 0.5*z),
                            jointAxis = str(jx)+" "+str(jy)+" "+str(jz)
                            ) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not finished here, haven't made random direction of it
            

            ## first body in the limb 
            sx = self.chromosome_bodysize[limb][0]
            sy = self.chromosome_bodysize[limb][1]
            sz = self.chromosome_bodysize[limb][2]
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
                    x = -self.chromosome_bodydirection[limb][3*body]
                    y = self.chromosome_bodydirection[limb][3*body+1]
                    z = self.chromosome_bodydirection[limb][3*body+2]
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
                    sx = c.scaler**(body)*self.chromosome_bodysize[limb][3*body]
                    sy = c.scaler**(body)*self.chromosome_bodysize[limb][3*body+1]
                    sz = c.scaler**(body)*self.chromosome_bodysize[limb][3*body+2]
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
                    pyrosim.Send_Sensor_Neuron(name = flag , linkName = "limb" + str(limb+self.limbnumber) + "link"+ str(body))
                    flag=flag+1


        ###############################################################
        ### mortor neurons (on joints)
        for limb in range (self.limbnumber):
            pyrosim.Send_Motor_Neuron( name = flag , jointName ="Torso_limb" + str(limb) + "link0")
            flag=flag+1
            pyrosim.Send_Motor_Neuron( name = flag , jointName ="Torso_limb" + str(limb+self.limbnumber) + "link0")
            flag=flag+1
            if self.number_of_limbbody[limb]>1:
                for body in range(1,self.number_of_limbbody[limb]):
                    pyrosim.Send_Motor_Neuron( name = flag , jointName ="limb" + str(limb) + "link"+ str(body-1) + "_" + "limb" + str(limb) + "link"+ str(body))
                    flag=flag+1
                    pyrosim.Send_Motor_Neuron( name = flag , jointName = "limb" + str(limb+self.limbnumber) + "link"+ str(body-1) + "_" + "limb" + str(limb+self.limbnumber) + "link"+ str(body))
                    flag=flag+1

        ###############################################################    
        #generate synapses
        for currentRow in range(self.totalsensornumber): #name of sensor neurons
            for currentColumn in range(self.totalmotornumber): #name of motor neurons
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
