#%%
import sys
from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(directOrGUI,solutionID) 
simulation.RUN(directOrGUI) # let the robot run
#print("run finished!!!!!!!!!!!!!!!!!!!!!!!")

simulation.Get_Fitness(solutionID) # measure the final distance the robot move
#print("fit finished")


# %%
