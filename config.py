import sim
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID !=-1:
    print ('Connected to remote API server')
else:
    print ('Failed connecting to remote API server')
sim.simxGetPingTime(clientID)
# sim.simxFinish(clientID)
ret, qd = sim.simxGetObjectHandle(clientID, 'qd_1', 
                  sim.simx_opmode_blocking)
ret, p = sim.simxGetObjectPosition(clientID, qd, -1, sim.simx_opmode_blocking)
ret, v, w = sim.simxGetObjectVelocity(clientID, qd, -1, sim.simx_opmode_blocking)
ret, r = sim.simxGetObjectOrientation(clientID, qd, -1, sim.simx_opmode_blocking)
# ret, w = sim.simxGetObjectQuaternion(clientID, qd, -1, sim.simx_opmode_blocking)
force = 1.0 # 推力值，可以根据需要修改 
torque = 4.0 # 目标位置的Z值，可以根据需要修改 # 发送信号到CoppeliaSim
i = 0
while i<100: 
    sim.simxSetFloatSignal(clientID, 'F', force, sim.simx_opmode_oneshot) 
    sim.simxSetFloatSignal(clientID, 'T', torque, sim.simx_opmode_oneshot)
    i = i + 1
# sim.addForceAndTorque(clientID, qd, force, torque, sim.simx_opmode_blocking)
sim.simxFinish(clientID)