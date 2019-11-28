# High Level Controller

##Overview 

The control-high repository consists of the High-Level Controller and the MHIST submodule of the SOZO Robotics Project.

The High-Level Controller (HLC) receives the area to cover from the Swarm Algorithm (tbd, currently mocked), gets updates about the local map and the current position in the map from [SLAM](https://github.com/codeuniversity/slam) and feedback about the (sucessful) leg movement from the [gait controller](https://github.com/codeuniversity/control-gait).
The Planning Alogorithm creates the high level actions (hla) to ensure a sucessful exploration of the area the robot should cover. These actions are forwarded to the gait controller.

## Project Structure

![hlc_sequence_diagram](./images/hlc_sequence_diagram.png)

The Monitor is the main Process, that is starting the subprocesses "Queues", "Receiver", "Supplier" and "Plan". The receiver subscribes to MHIST, a simple on disc measurement data base that stores and redistributes measurements consisting of a name, a value and optionally a timestamp through grpc.

##Requirements

Python version, packages etc --> requirement.txt
[MHIST](https://github.com/alexmorten/mhist/tree/2b4bed690fb6b38bf6e0c13f7b4f67c05c5d9c52 ) 

[Nervo](https://github.com/codeuniversity/nervo)

## Usage

Clone repository with submodules:

 ```git clone --recurse-submodules https://github.com/codeuniversity/control-high.git```



TBD

[Nervo](https://github.com/codeuniversity/nervo) to read and send message and to flash on the 

