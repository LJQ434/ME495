#%%
import pyrosim.pyrosim as pyrosim
import numpy
import simulate

class SOLUTION:

    def __init__(self):

        self.weights = 2 * numpy.random.rand(3,2) - 1
        #print(self.weights)
    

    def Evaluate(self,directOrGUI):

        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        pyrosim.End()

        simulate.main(directOrGUI)
        f = open("fitness.txt","r")
        self.fitness = float(f.read())
        #print('fitness is:',self.fitness) # print fitness
        f.close()
        

    
    def Create_World(self):

        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0,2,0.5] , size=[1,1,1])
        pyrosim.End()
        

    def Generate_Body(self):

        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[1,1,1])
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.5,0,1.0] )
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[1,1,1])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5,0,1.0] )
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[1,1,1])
        pyrosim.End()


    def Generate_Brain(self):

        #generate neurons
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        
        #generate synapses
        for currentRow in range(3): #name of sensor neurons
            for currentColumn in range(2): #name of motor neurons
                pyrosim.Send_Synapse( sourceNeuronName = currentRow ,
                 targetNeuronName = currentColumn + 3 , 
                 weight = self.weights[currentRow][currentColumn] )
    

    def Mutate(self):
        randomRow = numpy.random.randint(1,3)
        randomColumn = numpy.random.randint(1,2)
        self.weights[randomRow,randomColumn] = 2 * numpy.random.random() - 1
# %%
