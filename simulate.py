#%%
import pybullet_data
import pybullet as p
import time as t
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
RobotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
for i in range (1000):
    p.stepSimulation()
    t.sleep(0.05)
p.disconnect()
# %%
