#%%
import matplotlib.pyplot as plt
import numpy
import constants as c

f = open("bestfitness.txt","r")
fitness = (f.read()).split()
bestfitness = numpy.zeros((c.populationSize, c.numberOfGenerations), dtype = float)
bestbest = numpy.zeros((c.numberOfGenerations,1), dtype = float)
x={}

for pop in range(c.populationSize):
    for gen in range(c.numberOfGenerations):
        bestfitness[pop][gen] = fitness[pop*c.numberOfGenerations+ gen]

for gen in range(c.numberOfGenerations):
    for pop in range(c.populationSize):
        if bestfitness[pop][gen] >= bestbest[gen]:
            bestbest[gen] =bestfitness[pop][gen]
        
        
x= list(range(c.numberOfGenerations))
print(x)
print(bestfitness)

for pop in range(c.populationSize):
    plt.plot(x, bestfitness[pop] )
# %%
