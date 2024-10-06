import torch
import torch.nn as nn
from torch.autograd import Variable
import pdb
import numpy as np

def PreprocessData():
    
    SensorData = np.loadtxt('./SensorData/SensorData.txt')
    # Mark how many steps beforehand the collision needs to be predicted
    SensorDataRows = []
    for i in range(20):
        SensorDataRows.append(np.roll(SensorData[:,-1],-i-1))
    for i in range(20):
        SensorData[:,-1] += SensorDataRows[i]
    np.savetxt('./SensorData/LabeledSensorData.txt',SensorData)
    CollisionFullData = SensorData[ SensorData[:,-1] > 0 ]
    # Duplicating collision Data for faster learning    
    for i in range(10):
        SensorData = np.append(SensorData,CollisionFullData,axis=0)
    # Shuffle the sensor data
    np.random.shuffle(SensorData)
    SensorNNData = torch.Tensor(SensorData[:,:-1])
    CollisionData = torch.Tensor(CollisionFullData[:,:-1])
    SensorNNLabels = torch.Tensor(SensorData[:,-1]).view(-1,1)
    CollisionSensorNNLabels = torch.Tensor(CollisionFullData[:,-1]).view(-1,1)
    total = SensorNNData.shape[0]
    TrainSize = int(0.70*total)
    TestSize = total - TrainSize
    TrainSensorNNData = SensorNNData[:TrainSize]
    TrainSensorNNLabels = SensorNNLabels[:TrainSize]
    
    return TrainSize,SensorNNData,SensorNNLabels
