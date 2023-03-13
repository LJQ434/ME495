#%%
from solution import SOLUTION
import numpy
import constants as c
import copy
import os


class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        hc=0
        self.parents = {}
        self.children = {}
        self.directOrGUI="DIRECT"
        self.nextAvailableID = 0
        self.bestsolution = SOLUTION(self.nextAvailableID)
        for key in range (c.populationSize):
            self.parents[key] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
        self.bestfitness = numpy.zeros((c.populationSize, c.numberOfGenerations), dtype = float)
    #############################################################################
    #  evolve (evaluate, spawn, mutate, select)
    ##############################################################################
         
    def Evolve(self):
        
        self.Evaluate(self.parents)

        self.directOrGUI="DIRECT"
        for generation in range (c.numberOfGenerations):
            print("generation:",generation)
            self.Evolve_For_One_Generation(self.directOrGUI,generation)
        
        self.Show_Best()
        
        ################################################################

    def Evolve_For_One_Generation(self,directOrGUI,generation):
        
        self.Spawn()
        self.Mutate(generation)
        self.Regenerate() # body and brain update
        self.Evaluate(self.children)
        self.print() #print parent and children in a line
        self.Select(generation)
    
        ################################################################
    
    def Evaluate(self,solutions):

        for ID in range (c.populationSize):
            solutions[ID].Start_Simulation(self.directOrGUI,ID) 
        for ID in range (c.populationSize):
            solutions[ID].Wait_For_Simulation_To_End(self.directOrGUI,ID)
    
        ################################################################
    
    def Spawn(self):

        for ID in range (c.populationSize):
            self.children[ID] = copy.deepcopy(self.parents[ID])
    
        ################################################################
    
    def Mutate(self,generation):

        for ID in range (c.populationSize):
            self.children[ID].Mutate(generation)
        #print('parent weight=',self.parent.weights)
        #print('child weight=',self.child.weights)
    
        ################################################################
    def Regenerate(self):
        for ID in range (c.populationSize):
            self.children[ID].Generate_Body
            self.children[ID].Generate_Brain

    def Select(self,generation):

        #print('fitness pair:',self.parent[ID].fitness, self.child[ID].fitness)
        for ID in range (c.populationSize):
            if self.children[ID].fitness > self.parents[ID].fitness:
                self.parents[ID] = self.children[ID]
                print("forgroup",ID,":","child win")
            else:
                print("forgroup",ID,":","parent win")
            self.bestfitness[ID][generation] =  self.parents[ID].fitness
        

    ##############################################################################
    #  show and print
    ##############################################################################    

    def Show_Best(self):
        self.directOrGUI="DIRECT"  
        self.Evaluate(self.parents)
        self.bestsolution =  copy.deepcopy(self.parents[0])
        self.bestid = 0
        for ID in range (c.populationSize):
            if self.parents[ID].fitness >= self.bestsolution.fitness:
                 self.bestsolution =  copy.deepcopy(self.parents[ID])
                 self.bestsolution.fitness = self.parents[ID].fitness
                 self.bestid = ID
        print("the best is:",self.bestid,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
      

        

        ### find best solution's body and brain file and save them
        for ID in range (c.populationSize):
            if ID == self.bestid:
                if os.path.isfile('body.urdf'):
                    os.system("del body.urdf") 
                if os.path.isfile('brain.nndf'):
                    os.system("del brain.nndf") 
                os.rename("body"+str(ID)+".urdf" , "body.urdf")
                os.rename("brain"+str(ID)+".nndf" , "brain.nndf")
            else:
                 os.system("del body"+str(ID)+".urdf") 
                 os.system("del brain"+str(ID)+".nndf") 
        
        if os.path.isfile('body0.urdf'):
            os.system("del body0.urdf") 
        if os.path.isfile('brain0.nndf'):
            os.system("del brain0.nndf") 
        os.rename("body.urdf","body0.urdf")
        os.rename("brain.nndf","brain0.nndf")

        

        ###
        f = open("bestfitness.txt","w")
        for pop in range(c.populationSize):
            for gen in range(c.numberOfGenerations):
                f.write(str(self.bestfitness[pop][gen])) #distance it moves
                f.write(' ')
            
        #  ### save shape parameters  
        # f = open("bestshape.txt","w")
        # f.write(str(self.parents[self.bestid].bodynumber)) # how many bodies 
        # f.write(' ')
        # for i in range(self.bestsolution.bodynumber):
        #     for j in range (3):
        #         f.write(str(self.parents[self.bestid].bodysize[j][i])) #xyz size of each body
        #         f.write(' ')
        # f.close()    

        # ### save sensor distribution
        # f = open("bestsensorplan.txt","w")
        # for i in range(self.bestsolution.bodynumber):
        #     f.write(str(self.parents[self.bestid].sensorstatus[i])) #sensor distribution
        #     f.write(' ')
        # f.close()    

        self.bestsolution.Only_simulate("GUI",0)    


        ################################################################

    def print(self):
        for ID in range (c.populationSize):
            print("for group",ID,", fitness is: (",self.parents[ID].fitness,",", self.children[ID].fitness ,")")


    
# %%
