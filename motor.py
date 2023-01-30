#%%

import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self,Name):
        self.jointName = Name
    
    def Prepare_To_Act(self):
        self.amplitude = 0
        self.phaseOffset = 0
        self.frequency = 0
        self.force = 28
        self.motorValues = numpy.zeros(c.iter)
    
    def Save_Values(self):
        numpy.save('motor_value_b'+str(self.jointName),self.motorValues)


# %%
