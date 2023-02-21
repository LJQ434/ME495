#%%
from solution import SOLUTION
import constants as c
import copy
import os


class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        hc=0
        self.parents = {}
        self.children = {}
        self.directOrGUI="GUI"
        self.nextAvailableID = 0
        self.bestsolution = SOLUTION(self.nextAvailableID)
        for key in range (c.populationSize):
            self.parents[key] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    #############################################################################
    #  evolve (evaluate, spawn, mutate, select)
    ##############################################################################
         
    def Evolve(self):
        
        self.Evaluate(self.parents)

        self.directOrGUI="DIRECT"
        for i in range (c.numberOfGenerations):
            print("generation:",i)
            self.Evolve_For_One_Generation(self.directOrGUI)
        
        self.Show_Best()
        
        ################################################################

    def Evolve_For_One_Generation(self,directOrGUI):
    
        self.Spawn()
        self.Mutate()
        self.Regenerate() # body and brain update
        self.Evaluate(self.children)
        self.print() #print parent and children in a line
        self.Select()
    
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
    
    def Mutate(self):

        for ID in range (c.populationSize):
            self.children[ID].Mutate()
        #print('parent weight=',self.parent.weights)
        #print('child weight=',self.child.weights)
    
        ################################################################
    def Regenerate(self):
        for ID in range (c.populationSize):
            self.children[ID].Generate_Body
            self.children[ID].Generate_Brain

    def Select(self):

        #print('fitness pair:',self.parent[ID].fitness, self.child[ID].fitness)
         for ID in range (c.populationSize):
            if self.children[ID].fitness > self.parents[ID].fitness:
                self.parents[ID] = self.children[ID]
                print("forgroup",ID,":","child win")
            else:
                print("forgroup",ID,":","parent win")
    

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
        print("the best is:",self.bestid)
        print(self.bestsolution.weights)
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

        ### save synapses weight
        f = open("bestweight.txt","w")
        for i in range(self.bestsolution.sensornumber):
            for j in range(self.bestsolution.motornumber):
                f.write(str(self.parents[self.bestid].weights[i][j])) #distance it moves
                f.write(' ')
        f.close()  

         ### save shape parameters  
        f = open("bestshape.txt","w")
        f.write(str(self.parents[self.bestid].bodynumber)) # how many bodies 
        f.write(' ')
        for i in range(self.bestsolution.bodynumber):
            for j in range (3):
                f.write(str(self.parents[self.bestid].bodysize[j][i])) #xyz size of each body
                f.write(' ')
        f.close()    

        ### save sensor distribution
        f = open("bestsensorplan.txt","w")
        for i in range(self.bestsolution.bodynumber):
            f.write(str(self.parents[self.bestid].sensorstatus[i])) #sensor distribution
            f.write(' ')
        f.close()    

        self.bestsolution.Start_Simulation("GUI",ID)     


        ################################################################

    def print(self):
        for ID in range (c.populationSize):
            print("for group",ID,", fitness is: (",self.parents[ID].fitness,",", self.children[ID].fitness ,")")


    
# %%
