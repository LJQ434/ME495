#%%
from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):
        hc=0
        self.parent = SOLUTION()
        self.child = SOLUTION()
        self.directOrGUI=1
        #print(self.parent.weight)
        
    def Evolve(self):
        # first generation
        print('the first is as shown')
        self.parent.Evaluate(self.directOrGUI)
        
        # evolve
        for currentGeneration in range (c.numberOfGenerations):
            self.directOrGUI=0
            print('iteration = ',currentGeneration)
            self.Evolve_For_One_Generation(self.directOrGUI)
        
        # final generation
        print('the best is as shown')
        self.Show_Best()

    def Evolve_For_One_Generation(self,directOrGUI):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate(directOrGUI)
        self.Select()
    
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        #print('parent weight=',self.parent.weights)
        #print('child weight=',self.child.weights)

    def Select(self):
        print('fitness pair:',self.parent.fitness, self.child.fitness)
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child
            print('child win')
        else:
            print('parent win')
        
    def Show_Best(self):
        self.directOrGUI=1
        self.parent.Evaluate(self.directOrGUI)



    
# %%
