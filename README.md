# Emergency Vehicle Management System

## Overview

The Emergency Vehicle Management System is a hardware project aimed at addressing the critical issue of delayed ambulance response times, which often result in loss of lives. The inspiration behind this project is the alarming statistics in India, where one in 10 patients dies on the way to the hospital, with a significant portion of these deaths attributed to ambulances being held up by traffic.

## Problem Statement

Every day, an estimated 24,012 patient lives are lost due to traffic delays faced by ambulances. In road accidents, 30% of the 1,46,133 fatalities are caused by delayed ambulance arrivals. Additionally, more than 50% of heart attack cases reach the hospital late because patients are stuck in traffic. The existing systems have proven inadequate in handling these life-threatening situations.

## Solution

The key concept of the Emergency Vehicle Management System is the implementation of a "Virtual Ambulance." This virtual ambulance is initiated before the actual ambulance begins its journey. Leveraging advanced algorithms, the virtual ambulance predicts the path the driver will take and takes proactive measures to clear the path by overriding traffic signals.

## Features

- **Virtual Ambulance Activation**: The system initiates a virtual ambulance ahead of the actual ambulance departure to optimize the route and minimize response time.
  
- **Path Prediction Algorithm**: Utilizes advanced algorithms to predict the ambulance's route based on historical data and real-time traffic conditions.

- **Traffic Signal Override**: The virtual ambulance communicates with traffic signals along the predicted route to ensure they are in sync with the ambulance's path, allowing for a clear passage.
## Simulation
link to SUMO visual: https://drive.google.com/file/d/1z6Oewitzds_NI-zxpppx_w6qa0mYoobG/view?usp=sharing

## Technologies Used

The Emergency Vehicle Management System is built with the following technologies:

- **Arduino**: Used for hardware control and interfacing with sensors.

- **Mathplot**: Employed for visualizing data and path predictions.

- **NetworkX**: Utilized for graph-based algorithms to optimize ambulance routes.

- **Python**: The main programming language for system logic and algorithm implementation.

- **ROS (Robot Operating System)**: Implemented for communication between different system components.

