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
        self.force = 0
        self.motorValues = numpy.zeros(c.iter)
    
    def Set_Value(self,a,p,f,F):
        self.amplitude = a
        self.phaseOffset = p
        self.frequency = f
        self.force = F
        for i in range (c.iter):
            self.motorValues[i] = self.amplitude * numpy.sin(self.frequency * i + self.phaseOffset)
    
    def Save_Values(self):
        numpy.save('motor_value_b'+str(self.jointName),self.motorValues)

