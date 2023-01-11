#%%
import pybullet_data
import numpy 
import pybullet as p
import pyrosim.pyrosim as pyrosim
import time as t

physicsClient = p.connect(p.GUI)

# initialization
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
RobotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(RobotId)

iteration=1000
backLegSensorValues = numpy.zeros(iteration)
frontLegSensorValues = numpy.zeros(iteration)
targetAngles_back=numpy.zeros(iteration)
targetAngles_front=numpy.zeros(iteration)

amplitude_b=1*numpy.pi/4
frequency_b=2*numpy.pi/iteration*10
phaseOffset_b=0

amplitude_f=1*numpy.pi/4
frequency_f=2*numpy.pi/iteration*10
phaseOffset_f=0

# main loop
for i in range (iteration):
    p.stepSimulation()
    
    #sensor
    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] =  pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] =  pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    #motor 
    #x = numpy.linspace(0, 2*numpy.pi, iteration)
    #targetAngles = numpy.pi/4*numpy.sin(x)
    targetAngles_back[i] = amplitude_b * numpy.sin(frequency_b * i + phaseOffset_b)
    targetAngles_front[i] = amplitude_f * numpy.sin(frequency_f * i + phaseOffset_f)

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = RobotId,
    jointName = b"BackLeg_Torso",
    controlMode = p.POSITION_CONTROL,
    targetPosition = targetAngles_back[i],
    maxForce = 28)

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = RobotId,
    jointName = b"Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = -targetAngles_front[i],
    maxForce = 28)

    # step time
    t.sleep(0.01)

p.disconnect()


# sensor value storage
print(backLegSensorValues)
print(frontLegSensorValues)
numpy.save('sensordata_back',backLegSensorValues)
numpy.save('sensordata_front',frontLegSensorValues)
numpy.save('motor_value_b',targetAngles_back)
numpy.save('motor_value_f',targetAngles_front)
# %%
