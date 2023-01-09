#%%
import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[0,2,0.5] , size=[1,1,1])
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5] , size=[1,1,1])
    pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.5,0,1.0] )
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,0.5] , size=[1,1,1])
    pyrosim.Send_Joint(name = "FrontLeg_BackLeg" , parent= "FrontLeg" , child = "BackLeg" , type = "revolute", position = [1,0,0] )
    pyrosim.Send_Cube(name="BackLeg", pos=[0.5,0,-0.5] , size=[1,1,1])
    pyrosim.End()


# main
Create_World()
Create_Robot()
# %%