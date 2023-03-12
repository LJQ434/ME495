#%%
import constants as c
from solution import SOLUTION
import numpy

best = SOLUTION(0)

### load body number and shape 
f = open("bestshape.txt","r")
shape = (f.read()).split()

f.close()
best.bodynumber = int(shape[0])
print(best.bodynumber)
bestbodysize = numpy.zeros((3,best.bodynumber))
for i in range (best.bodynumber):
    for j in range (3):
        bestbodysize[j][i]= float(shape[1+3*i+j])
best.bodysize = bestbodysize

### load neuron distirbution
f = open("bestsensorplan.txt","r")
sensorplan = (f.read()).split()
f.close()
bestsensorplan=numpy.zeros(best.bodynumber)
for i in range (best.bodynumber):
    bestsensorplan[i] = int(sensorplan[i])
best.sensorstatus = bestsensorplan
best.sensornumber = int(sum(best.sensorstatus))
print(best.sensornumber)
best.motornumber = best.bodynumber - 1

### load best weight
#read synapsis weight
f = open("bestweight.txt","r")
weights = (f.read()).split()
f.close()

bestweights = numpy.zeros((best.sensornumber,best.motornumber))
for i in range(best.sensornumber):
    for j in range(best.motornumber):
        bestweights[i][j]=float(weights[best.motornumber*i+j]) #import the best weights

best.weights = bestweights


print(best.weights)

best.Start_Simulation("GUI",0) #import the best: body0.urdf and brain0.nndy

# %%
