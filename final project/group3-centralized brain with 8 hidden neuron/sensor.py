#%%
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c


class SENSOR:
    def __init__(self,Name):
        self.linkName = Name
        self.value = numpy.zeros(c.iter)
        
    def Get_Value(self,t):
        self.value[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #print(self.value[t])

    def Save_Values(self):
        numpy.save('sensordata_'+str(self.linkName),self.value)
        
# %%
