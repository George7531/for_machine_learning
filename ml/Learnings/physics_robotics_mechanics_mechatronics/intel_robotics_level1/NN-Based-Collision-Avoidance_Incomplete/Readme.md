Predictive Model For Collision Avoidance
============================================================
This is a simulator for the tutorial on collision-detection using a feedforward neural network from Interactive Robotics Lab at Arizona State University.


Requirements
-------------------------------------------------------------
- The code can be run in Python2.7 and all versions of Python3 
- For smooth installation on Windows, Linux and Mac. It is recommended to install anaconda from here https://www.anaconda.com/download/
- Please run the following commands after installing anaconda

``````````````
conda create -name intel_game_env python=3.6
source activate intel_game_env   ## Windows -> conda activate intel_game_env 
conda install pytorch-cpu -c pytorch 

pip install cython
pip install torchvision
pip install pygame
pip install pymunk

`````````````` 


Description of files
---------------------------------------------------------------
Files that should NOT be edited:

Filename                          |  Description
----------------------------------|------------------------------------------------------------------------------------
ExploreAndCollect.py              |  Takes random actions in the simulator and collects the collision details.
PlayingTheModel.py                |  Loads the learned network and acts based on the neural network output
PreProcessing.py                  |  Process sensor data to train with neural network

Files that can be edited:

Filename                          |  Description
----------------------------------|------------------------------------------------------------------------------------
MakeItLearn.py                    |  Trains the neural network



Usage
---------------------------------------------------------------

To run this project. Please do the following steps


``````````````
python ExploreAndCollect.py

``````````````
It opens up the simulator. The bot drives around randomly, sometimes bumping into the walls. All the sensor data during this simulation is collected and stored in 'sensor_data/sensor_data.txt'



``````````````
python MakeItLearn.py

``````````````
This program does three things:
 
1. Loads the sensor data collected and labels all the collision data as 1 and the rest of them as 0.
2. Creates a feedforward neural network and trains with labeled data up to 25 epochs. 
3. Stores the trained model as 'saved_nets/nn_bot_model.pkl'


``````````````
python PlayingTheModel.py

``````````````
This program loads the neural network model and opens up the simulator. The bot is programmed to drive itself to the destination and feeding the sensor data to the neural network at everytime step.
If the neural network detects collision bot turns green and takes alternative action, to the action it was planning to take.



Optional
---------------------------------------------------------------

After running the above commands, to have different start position; run any of the commands below

``````````````
python PlayingTheModel.py 1

``````````````

``````````````
python PlayingTheModel.py 2

``````````````


``````````````
python PlayingTheModel.py 3

``````````````


``````````````
python PlayingTheModel.py 4

``````````````
