#%%
import constants as c
from solution import SOLUTION
import numpy

best = SOLUTION(0)
f = open("bestsolution.txt","r")
weights = (f.read()).split()
f.close()
for i in range(c.numSensorNeurons):
    for j in range(c.numSensorNeurons):
        best.weights[i][j]=float(weights[c.numSensorNeurons*i+j])

print(best.weights)
best.Start_Simulation("GUI",0)
