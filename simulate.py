#%%
from simulation import SIMULATION

def main():
    simulation = SIMULATION()
    simulation.RUN()
    simulation.__del__()
    print("finished")

main()

# %%
