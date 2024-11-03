# Unimelb COMP90054 Reversi Agents

## Acknowledgment

I would like to thank the Unimelb COMP90054 2022S2 teaching team for providing the code framework and the opportunity to explore various AI techniques in this project.

## Project Introduction

In this project, we will design several autonomous agents capable of playing the Reversi game on their own and compare their performances. This comparison will allow us to analyze the effectiveness of different strategies and algorithms, helping us identify the best approaches for optimizing the agents' gameplay.

All the code we implemented is located in the directory `/agents/myAgent/`. The rest of the code framework has been provided by the teaching staff of Unimelb COMP90054 2022 Semester 2.

## Reversi Game Introduction

Reversi, also known as Othello, is a classic board game played on an 8x8 grid. The game is designed for two players, each of whom takes on the role of either black or white. The objective is to have the majority of your pieces on the board by the end of the game.

### Game Rules

1. **Setup** : At the beginning of the game, four discs are placed in the center of the board in a square formation, with two black discs and two white discs diagonally opposite each other.
2. **Gameplay** : Players take turns placing their discs on the board. A player can only place a disc in a position that will "sandwich" one or more of the opponent's discs between their own discs—this means that the opponent's discs must be in a straight line (horizontally, vertically, or diagonally) and be surrounded by the player's discs on both ends.
3. **Flipping Discs** : When a player successfully sandwiches the opponent's discs, those discs are flipped to the player's color. This mechanic is a key strategic element of the game, as it can dramatically change the board's landscape.
4. **End of the Game** : The game continues until neither player can make a valid move, which usually occurs when the board is full. The player with the most discs of their color at the end of the game wins.

### Strategy

Reversi is a game of strategy that requires foresight and planning. Players must consider not only their moves but also how those moves will affect the opponent's options. Controlling the corners of the board is particularly advantageous, as corner discs cannot be flipped.

Reversi's simple rules combined with its deep strategic complexity make it a popular choice for both casual players and competitive gaming.

## My Agents

We designed four distinct agents for the Reversi project, each employing different strategies and algorithms:

1. **Uniform Cost Search (UCS) Agent**
2. **Reinforcement Learning Agent**
3. **Monte Carlo Tree Search (MCTS) Agent**
4. **Game Theory MinMax Agent**

### 1. Uniform Cost Search (UCS) Agent

The UCS Agent for Reversi uses the Uniform Cost Search algorithm to choose moves based on the score difference with the opponent. It has a time limit for making decisions and looks for the best possible game states to explore. By simulating potential moves, the agent selects actions that aim to increase its score while reducing the opponent's chances. It prioritizes the best move it finds within the time allowed, making it a strategic player in the game.

### 2. Reinforcement Learning Agent

The RL Agent for Reversi uses reinforcement learning to improve its gameplay. It calculates features like scores and corner control to evaluate possible moves. The agent selects actions based on their Q-values, which are updated using a learning process after each game. It balances exploration and exploitation with an epsilon-greedy strategy, allowing it to learn from experience and adapt its decisions over time.

### 3. Monte Carlo Tree Search (MCTS) Agent

The MCTS Agent for Reversi uses the Monte Carlo Tree Search algorithm to decide its moves. It explores possible game states by simulating random plays and evaluates the outcomes based on the scores. The agent maintains records of state values, visit counts, and best actions. It selects moves through a process of selection, expansion, simulation, and backpropagation, continually updating its understanding of which actions lead to better results. This allows the agent to make informed decisions within a given time limit.

### 4. Game Theory MinMax Agent

The Game Theory MinMax Agent for Reversi uses the Alpha-Beta pruning technique to optimize move selection. It evaluates game states to determine the best possible action based on a heuristic table that scores board positions. The agent recursively explores potential future moves, maximizing its score while minimizing the opponent's score. If the time limit is reached or a maximum depth is hit, it returns the best action found. This approach allows the agent to make informed decisions by simulating the opponent's responses and optimizing its strategy accordingly.

## Code Instructions

### **Install Dependencies**

Ensure you have the necessary dependencies installed. You may need to set up a virtual environment and install required packages listed in `requirements.txt`.

### Demonstration Program

After cloning the repository to your local machine, you can run the following command in the terminal. 

```bash
$ python general_game_runner.py
```

This program features two random agents playing against each other, serving only demonstration purposes, as the random agents do not employ any strategies.

### Run Game with Agents

The following command allows two agents to compete against each other.

```bash
$ python3 general_game_runner.py -a Agent1, Agent2
```

The agents: `Agent1` and `Agent2` can be choose from:

* `agents.generic.random`: Agent that takes random actions
* `agents.generic.first_move`: Agent that takes first action among all possible actions
* `agents.generic.timeout`: Agent that takes first action among all possible actions, with 2 second waiting time
* `agents.myAgents.mctAgent`: Monte Carlo Tree Search Agent
* `agents.myAgents.rlAgent`: Reinforcement Learning Agent
* `agents.myAgents.minmaxAgent`: Game Theory MinMax Agent
* `agents.myAgents.ucsAgent`: Uniform Cost Search Agent

## Agents Performance

### Agents Performance Overview

The performance of the Reversi agents was evaluated through a series of matches against each other and against random players. Each agent demonstrated unique strengths and weaknesses, which were influenced by the algorithms employed.

1. **UCS Agent** : The Uniform Cost Search agent performed well in scenarios with predictable opponent behavior, effectively maximizing its score by exploring the most beneficial moves. However, it struggled against more aggressive strategies due to its reliance on immediate costs rather than long-term planning.
2. **Reinforcement Learning Agent** : The RL agent showed improvement over time, adapting its strategy based on past experiences. Initially, it faced challenges in decision-making but became more effective in controlling the board as it learned from multiple games. Its performance highlighted the importance of exploration in finding optimal strategies.
3. **Monte Carlo Tree Search Agent** : The MCTS agent excelled in complex situations where numerous possible moves were available. Its ability to simulate random outcomes allowed it to discover effective strategies, resulting in competitive performance against other agents. However, its performance was sometimes limited by the time constraints imposed on decision-making.
4. **Game Theory MinMax Agent** : The MinMax agent consistently produced strong results, effectively countering opponents by anticipating their moves and maximizing its score. Its use of heuristic evaluation enabled it to make informed decisions quickly. However, it sometimes struggled with deeper game states due to the computational limits of the Alpha-Beta pruning approach.

Overall, the agents demonstrated varied levels of effectiveness depending on the strategies employed and the nature of their opponents. The experiments provided valuable insights into the strengths of different algorithms and the importance of adapting strategies in competitive environments.

### Head-to-Head Matches

To assess the relative performance of the agents, we conducted 100 matches between each pair of agents. The results were as follows:

| Result (vertical vs. horizontal) | UCS Agent | RL Agent  | MCTS Agent | MinMax Agent |
| -------------------------------- | --------- | --------- | ---------- | ------------ |
| **UCS Agent**              | -         | 43 vs 57 | 40 vs 60   | 12 vs 88     |
| **RL Agent**               |           | -         | 55 vs 45   | 24 vs 76     |
| **MCTS Agent**             |           |           | -          | 8 vs 92     |
| **MinMax Agent**           |           |           |            | -            |

### Final Competition

The MinMax agent, selected as the strongest performer, participated in a series of matches against agents from other groups. It achieved an impressive rank of 10/192, demonstrating its effectiveness and robustness in a competitive environment. The MinMax agent's ability to predict opponent moves and optimize its strategy contributed significantly to its success.

## Conclusion

In conclusion, the project successfully implemented multiple Reversi agents using different artificial intelligence techniques, including Uniform Cost Search, Reinforcement Learning, Monte Carlo Tree Search, and Game Theory MinMax. Each agent showcased distinct approaches to gameplay, resulting in a diverse set of strategies that contributed to the overall understanding of AI in game scenarios.

The results indicated that while some agents excelled in certain situations, adaptability and learning from experience were critical for success in a dynamic game environment. The Reinforcement Learning agent's performance improved significantly over time, emphasizing the effectiveness of learning-based approaches. Meanwhile, the MinMax agent's strategic foresight demonstrated the value of game theory in decision-making.

Future work could focus on further refining these agents by integrating hybrid strategies or enhancing their learning algorithms. Additionally, exploring more advanced techniques such as deep reinforcement learning could provide even greater insights into optimizing performance in Reversi and other strategic games.
