# Dynamics-Physics-Simulator

A Pygame-based simulator that visualizes a block sliding down a frictional inclined plane, calculating its motion in real time from user-supplied angle and friction values.

## How it works

* The player enters an incline angle in degrees, greater than 33, and a coefficient of friction, greater than 0, through console prompts that are mirrored as text on the simulation window.
* A right triangle is drawn on screen using the chosen angle and a fixed height, representing the inclined plane the block will slide down.
* A rotated rectangle representing the block starts at the top of the incline and is animated downward each frame, with its motion driven by a simplified force model combining gravitational acceleration with a friction-scaled horizontal and vertical component.
* Once the block reaches the bottom vertex of the triangle, the simulation freezes it in place and computes the time taken and final velocity using standard kinematics, incorporating gravity, the incline angle, and friction into the acceleration term.
* The computed time and velocity are printed to the console, and the player is then asked whether they would like to run another calculation with new inputs.
* Invalid numeric input at either prompt triggers an on-screen error message before the prompt is shown again.

## Tech stack

The simulator is written in Python and relies on the Pygame library for windowing, rendering, event handling, and timing, along with the standard math module for trigonometric and kinematic calculations.

## Project structure

```
dynamics-physics-simulator/
└── DynamicsPhysicsSimulator.py
```

## Running it locally

Clone the repository, install Pygame, and run the script directly:

```
git clone https://github.com/your-username/dynamics-physics-simulator.git
cd dynamics-physics-simulator
pip install pygame
python DynamicsPhysicsSimulator.py
```

## Design notes

The incline triangle is recalculated from scratch for every run based on the entered angle, since its base length is derived from a fixed height divided by the tangent of the angle, keeping the triangle proportioned correctly regardless of input. The block surface is built separately from its rotation, drawn flat and then rotated with Pygame's transform utilities, so that its visual orientation matches the slope of the incline.

## Contact

Haroon Riaz — haroonriaz116@gmail.com
