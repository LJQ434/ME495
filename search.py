#%%
import os
import generate
import simulate

for i in range(2):
    generate.main()
    simulate.main()
    #os.system("python3 generate.py")
    #os.system("python3 simulate.py")
    print(i)


# %%
