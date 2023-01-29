#%%
from simulation import SIMULATION

def main(directOrGUI):
    simulation = SIMULATION(directOrGUI) 
    simulation.RUN(directOrGUI) # let the robot run
    #print("run finished")
    simulation.Get_Fitness() # measure the final distance the robot move
    #print("fit finished")
    

#main()

# %%
