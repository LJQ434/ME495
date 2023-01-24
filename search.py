#%%
import os
import generate
import simulate

for i in range (2):
    
    print('iter=',i)
    
    os.system("python3 generate.py")
    os.system("python3 simulate.py")
    



# %%
