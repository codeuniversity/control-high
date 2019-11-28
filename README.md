# High-Level-Controller Exploration-Bot

This is part of the SOZO-Robotics Exploration-Bot architecture. See the other components of our Exploration-Bot architecture:

- [Low-Level-Controller](https://github.com/codeuniversity/control-low)
- [Gait-Controller](https://github.com/codeuniversity/control-gait)
- [SLAM](https://github.com/codeuniversity/slam)
- [Nervo](https://github.com/codeuniversity/nervo)
- Swarm (currently still WIP)

## Overview

The High-Level-Controller, further referred to as HLC, is responsible for navigating the robot.
In short, it receives orders from the Swarm, creates a plan to walk through the whole map and forwards movement actions to the Gait-Controller.

[architectural-overview.png](./architecural-overview.png)

## Description

The HLC consists of three main parts and one manager. There is the part responsible for creating the plan, the part responsible for receiving data and the part responsible for preparing and sending data. The manager is responsible for starting everything in the first place, keeping it alive and managing the cummunication between the other parts.

-- HERE COMES A DISCLAIMER --
At the moment many parts still have not been build or even fully planned yet. So some components or even bigger parts of the whole architecture might change drastically.

### Monitor

The Monitor will start all the different processes and run continuisly to ensure their full integrity. If some component fails, it will be restarted by the Monitor. The Monitor also handles the communication between the three other components.

### Planner

The Planner will take the size of the map and the location of the obstacles to create a plan/path through the given map. It will replan once the current plan is not possible anymore.

### Sender

The Sender will take the plan from the Planner and send it one action at a time to the Gait-Controller. When the Planner replans, the Sender will get the updated map and send the new actions.

### Receiver

The Receiver takes information about the boundaries of the map to cover from the Swarm to be used for the plan. It also takes data from SLAM about newly observed obstacles.

## Setup

There will be a setup repository linked here when it is finished. This repo will include our whole Exploration-Bot software bundled for easy deployment and use.

## Local development

__Requirements:__

- Python3.7
- The following pip modules:
  - grpc
  - pydocstyle

__Guidelines:__

- Activate pydocstyle as a linter and follow the ruels
- Activate pytest and always check that tests are passing before committing.
