# Agent tournament

## Overview
Agent tournament is a 2D 'capture the flag' python game with 2 agents; blue agent and red agent.

Both agents start at the opposite start of the world and their goal is to capture the enemy's flag and bring it back home whilst protecting their own.
While moving, agents have the ability to shoot at each other which can result in an agent dying.

## Features

### Agent states

An agent can have 1 of a select number of states. These states determine what the agent does at that moment.  
The states are:

* Spread state
    * The spread state is implemented so agents move away from each other at the start of the game. This ensures they don’t just follow each other around.
* Dodge state
    * The dodge state is responsible for ensuring agents move out of the way of incoming bullets.
* Capture state
    * This state keeps track of the previous moves of the agent and enforces a random move if they are in a cycle.
* Combat state
    * When agents see each other, they navigate towards each other and shoot.
* Support state
    * If an agent sees a teammate carrying the enemy flag, it follows that agent to defend them.
* Hunt state
    * If the agent returns home and their flag is missing, they enter the hunt state. This is because it means an enemy has got their flag.
* Bring state
    * If the agent has the enemy flag, a shortest path algorithm (breadth-first) is used to make it back home as fast as possible.
* Random state
    * The agent navigates around to where the flag is likely to be. If it can’t find it, it searches the whole world until it is entirely explored.

## Run

```python3 main.py```
