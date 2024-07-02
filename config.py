import sim
import numpy as np
import struct

# # sim.simxFinish(clientID)
# ret, qd = sim.simxGetObjectHandle(clientID, 'qd_1', 
#                   sim.simx_opmode_blocking)
# ret, p = sim.simxGetObjectPosition(clientID, qd, -1, sim.simx_opmode_blocking)
# ret, v, w = sim.simxGetObjectVelocity(clientID, qd, -1, sim.simx_opmode_blocking)
# ret, r = sim.simxGetObjectOrientation(clientID, qd, -1, sim.simx_opmode_blocking)
# # ret, w = sim.simxGetObjectQuaternion(clientID, qd, -1, sim.simx_opmode_blocking)
# force = 1.0 # 推力值，可以根据需要修改 
# torque = 4.0 # 目标位置的Z值，可以根据需要修改 # 发送信号到CoppeliaSim
# i = 0
# while i<100: 
#     sim.simxSetFloatSignal(clientID, 'F', force, sim.simx_opmode_oneshot) 
#     sim.simxSetFloatSignal(clientID, 'T', torque, sim.simx_opmode_oneshot)
#     i = i + 1
# # sim.addForceAndTorque(clientID, qd, force, torque, sim.simx_opmode_blocking)
# sim.simxFinish(clientID)
class config:
    def __init__(self, nq) -> None:
        sim.simxFinish(-1) # just in case, close all opened connections
        self.clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        if self.clientID !=-1:
            print ('Connected to remote API server')
        else:
            print ('Failed connecting to remote API server')
        sim.simxGetPingTime(self.clientID)
        self.qd = []
        for i in range(nq):
            ret, qdt = sim.simxGetObjectHandle(self.clientID, 'qd_'+str(i+1), 
                    sim.simx_opmode_blocking)
            self.qd.append(qdt)
            if ret == sim.simx_return_ok:
                print("Found quadcopter %s"%i)
            else:
                print("Quadcopter %s not found"%i)
        ret, self.pl = sim.simxGetObjectHandle(self.clientID, 'payload', 
                    sim.simx_opmode_blocking)
        if ret == sim.simx_return_ok:
            print("Found payload")
        else:
            print("Payloads not found")
        sim.simxSetStringSignal(self.clientID, 'start', 'e', sim.simx_opmode_oneshot_wait)
        # pass
    def getloadstate(self):
        _, p = sim.simxGetObjectPosition(self.clientID, self.pl, -1, sim.simx_opmode_blocking)
        _, v, w = sim.simxGetObjectVelocity(self.clientID, self.pl, sim.simx_opmode_blocking)
        _, q = sim.simxGetObjectQuaternion(self.clientID, self.pl, -1, sim.simx_opmode_blocking)
        pos = np.array([p]).T
        vel = np.array([v]).T
        qot = np.array([q]).T
        omg = np.array([w]).T
        pl_state = np.vstack((pos, vel, qot, omg))
        return pl_state
    def getqdstate(self, index):
        _, p = sim.simxGetObjectPosition(self.clientID, self.qd[index], -1, sim.simx_opmode_blocking)
        _, v, w = sim.simxGetObjectVelocity(self.clientID, self.qd[index], sim.simx_opmode_blocking)
        _, q = sim.simxGetObjectQuaternion(self.clientID, self.qd[index], -1, sim.simx_opmode_blocking)
        pos = np.array([p]).T
        vel = np.array([v]).T
        qot = np.array([q]).T
        omg = np.array([w]).T
        qd_state = np.vstack((pos, vel, qot, omg))
        return qd_state
    def fmcommand(self, index, thrust, torque):
        torque_packed = struct.pack('f' * len(torque), *torque)
        thrust_packed = struct.pack('f' * len(thrust), *thrust)
        # print(sim.simxUnpackFloats(torque_packed))
        sim.simxSetStringSignal(self.clientID, 'start', 's', sim.simx_opmode_oneshot_wait)
        sim.simxSetStringSignal(self.clientID,'torque_'+str(index+1), torque_packed, sim.simx_opmode_oneshot_wait)
        sim.simxSetStringSignal(self.clientID,'thrust_'+str(index+1), thrust_packed, sim.simx_opmode_oneshot_wait)
        # sim.simxSetStringSignal(self.clientID, 'start', 's', sim.simx_opmode_oneshot_wait)
    def stopsim(self):
        sim.simxSetStringSignal(self.clientID, 'start', 'e', sim.simx_opmode_oneshot_wait)
        sim.simxFinish(self.clientID)

if __name__ == "__main__":
    conf = config(1)
    pl1 = conf.getloadstate()
    # print(pl1)
    qd1 = conf.getqdstate(0)
    # print(qd1)
    thrust = np.array([0.0, 0.0, 2.0], dtype=np.float32)
    # print(type(thrust[0]))
    torque = np.array([0.0,0.0,0.0],dtype=np.float32)
    # thrust_packed = struct.pack('f' * len(torque), *torque)
    conf.fmcommand(0, thrust, torque)
    conf.stopsim()


