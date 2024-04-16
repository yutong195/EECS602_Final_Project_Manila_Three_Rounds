# AI Game Agent

State 402 coures project\
Reinforcement learing agents playing the board game [_Manile_](<https://en.wikipedia.org/wiki/Manila_(board_game)>).

## Description

We developed two agents using Q Learning and Deep Q network. Each agent has three different behaviors: normal, conservative, and aggressive.

Each agent supports playing with human or our evaluation benchamrk.

## Getting Started

### Prerequisites

- Python 3.10.8
- Pytorch 1.13.0
- Other pachages listed in the requirements.txt

### Installing

- Clone from Github

```
git clone git@github.com:SeekingAspdelus/AI_Game_Agent.git
```

- Install environment

```
pip install -r requirements.txt
```

### Executing programs

To train the agents

```
python Manila.py
```

Args supported:

- --mode: which algorithm to use, _Q_learning_ or _DQN_
- --epoch: how time the game will be executed
- --AI_num: number of AI players
- --verbose: whether to print the gaming details

To test agent on benchmark

```
python benchmark.py
```

Args supported:

- --mode: which algorithm to test, _Q_learning_ or _DQN_
- --epoch: how time the game will be executed
- --behavior: behavior of agent, _normal_, _conservative_, and _aggressive_
- --verbose: whether to print the gaming details

For people to play against AI ( only support 1 human player vs. 2 AI players with the same algorithm)

```
python human_AI_Combat.py
```

- --mode: which algorithm to test, _Q_learning_ or _DQN_
- --behavior1: behavior of the first AI, _normal_, _conservative_, and _aggressive_
- --behavior2: behavior of the second AI, _normal_, _conservative_, and _aggressive_

## File description

- _Manile_ game framework includes **_game.py, investment.py, play.py_**
- Q learning implementation: **_agents.py_**
- DQN implementation: **_dqn.py_**
- Benchmark implementation: **_benchmark_agent.py_**
- Agents training file: **_Manila.py_**
- Agents evaluation file: **_benchmark.py_**
- Human AI combat file: **_human_AI_Combat.py_**
- Helper functions: **_util.py_**

## Authors

Yutong Ren, yr55@duke.edu  
Jinxuan Zhang, jz332@duke.edu  
Tianle Zhu, tz100@duke.edu
