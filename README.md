# High Level Controller

## Overview

The control-high repository consists of the High-Level Controller and the MHIST submodule of the SOZO Robotics Project.

The High-Level Controller (HLC) receives the area to cover from the Swarm Algorithm (tbd, currently mocked), gets updates about the local map and the current position in the map from [SLAM](https://github.com/codeuniversity/slam) and feedback about the leg movement (successful/panic - leg x stuck) from the [gait controller](https://github.com/codeuniversity/control-gait).
The Planning Alogorithm outputs the high level actions that the robot will use to navigate through the area to completely explore it. You can test the algorithm with the pytests defined in ```hlc/tests```. The high level actions ("move forward" or "turn by 90 degrees") are sent to the gait controller.

## Project Structure

![hlc_sequence_diagram](./images/hlc_sequence_diagram.png)

The "Monitor" is the main Process, that is starting the subprocesses "Queues", "Receiver", "Supplier" and "Plan". The receiver subscribes to [MHIST](https://github.com/alexmorten/mhist/tree/2b4bed690fb6b38bf6e0c13f7b4f67c05c5d9c52), a simple on disk measurement data base that stores and redistributes measurements consisting of a sensor name and a value through grpc.
The output, the hla, are pushed to MHIST and then pulled from the gait controller.

## To Do

- [ ] Planning Algorithm
  - [x] no obstacles
  - [ ] obstacle avoidance
- [x] Tests for Planning Algorithm
- [ ] Grid Generator
- [ ] Monitor
- [x] Receiver with Queues
- [ ] Supplier



