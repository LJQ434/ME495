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
        
        
        #print(self.parent.weight)
        
    def Evolve(self):
        
        self.Evaluate(self.parents)

        self.directOrGUI="DIRECT"
        for i in range (c.numberOfGenerations):
            print("generation:",i)
            self.Evolve_For_One_Generation(self.directOrGUI)
        
        self.Show_Best()
    
    def Evaluate(self,solutions):
        for ID in range (c.populationSize):
            solutions[ID].Start_Simulation(self.directOrGUI,ID) 
        for ID in range (c.populationSize):
            solutions[ID].Wait_For_Simulation_To_End(self.directOrGUI,ID)

    def Evolve_For_One_Generation(self,directOrGUI):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.print() #print parent and children in a line
        self.Select()
        
    def Spawn(self):
        for ID in range (c.populationSize):
            self.children[ID] = copy.deepcopy(self.parents[ID])

    def Mutate(self):
        for ID in range (c.populationSize):
            self.children[ID].Mutate()
        #print('parent weight=',self.parent.weights)
        #print('child weight=',self.child.weights)

    def Select(self):
        #print('fitness pair:',self.parent[ID].fitness, self.child[ID].fitness)
         for ID in range (c.populationSize):
            if self.children[ID].fitness > self.parents[ID].fitness:
                self.parents[ID] = self.children[ID]
                print("forgroup",ID,":","child win")
            else:
                print("forgroup",ID,":","parent win")
        
    def Show_Best(self):
        self.directOrGUI="DIRECT"  
        self.Evaluate(self.parents)
        self.bestsolution =  copy.deepcopy(self.parents[0])
        for ID in range (c.populationSize):
            if self.parents[ID].fitness > self.bestsolution.fitness:
                 self.bestsolution =  copy.deepcopy(self.parents[ID])

        self.bestsolution.Start_Simulation("GUI",ID)     

    def print(self):
        for ID in range (c.populationSize):
            print("for group",ID,", fitness is: (",self.parents[ID].fitness,",", self.children[ID].fitness ,")")


    
# %%
