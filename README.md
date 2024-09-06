# Ultimate Tic-Tac-Toe MCTS Bot

## Authors
- Krisha Sharma [krvsharm]
- Nick Powell [nipowell]

## Description
This project implements a bot for playing Ultimate Tic-Tac-Toe using Monte Carlo Tree Search (MCTS). Two versions of the MCTS bot have been developed:
1. `mcts_vanilla.py`: Uses MCTS with full, random rollouts.
2. `mcts_modified.py`: Improves on the vanilla version with heuristic rollouts and other enhancements.

## Files
- `mcts_vanilla.py`: Implementation of the vanilla MCTS bot.
- `mcts_modified.py`: Implementation of the modified MCTS bot with heuristic rollouts.
- `p2_sim.py`: Multiple-game simulator for running rounds between pairs of bots.
- `p2_play.py`: Interactive version of the game.
- `mcts_node.py`: Defines the MCTSNode class used for constructing the game tree.
- `p2_t3.py`: Defines the Board class and game setup.

## Modifications in `mcts_modified.py`
The `mcts_modified.py` file includes several enhancements over the vanilla MCTS implementation:
1. **Heuristic Rollouts**: The rollout phase uses heuristic action selection instead of random action selection.
    - Winning moves are prioritized.
    - Blocking opponent's winning moves are prioritized.
    - Fallback to random action if no winning or blocking moves are available.
2. **Enhanced UCB Calculation**: Adjustments are made to the UCB function to better handle the opponent's turn.
3. **Improved Tree Traversal**: The tree traversal phase includes improved selection criteria to navigate the tree more efficiently.

# Experiment 1: Tree Size

## Objective
The objective of this experiment is to evaluate the performance of the vanilla MCTS bot with different tree sizes.

## Setup
- Player 1: Vanilla MCTS bot with a fixed tree size of 100 nodes.
- Player 2: Vanilla MCTS bot with varying tree sizes (50, 100, 200, 400 nodes).
- Number of games: 100 per tree size.

## Results
| Tree Size (Player 2) | Wins (Player 1) | Wins (Player 2) |
|----------------------|-----------------|-----------------|
| 50                   | 52              | 48              |
| 100                  | 50              | 50              |
| 200                  | 53              | 47              |
| 400                  | 70              | 30              |


## Analysis
- The performance of Player 2 initially improves slightly when increasing the tree size from 50 to 100 nodes.
- Beyond 100 nodes, Player 2's performance decreases as the tree size increases.
- This suggests that a larger tree size does not necessarily lead to better performance and may even degrade it beyond a certain point.
- See experiment1.pdf for detailed analysis.

## Conclusion
The vanilla MCTS bot performs better with a balanced tree size of around 100 nodes. Increasing the tree size beyond this point does not yield better results and may lead to performance degradation.

# Experiment 2: Heuristic Improvement

## Objective
The objective of this experiment is to compare the performance of the modified MCTS bot against the vanilla MCTS bot with equal tree sizes.

## Setup
- Player 1: Vanilla MCTS bot.
- Player 2: Modified MCTS bot with heuristic rollouts.
- Tree sizes tested: 200, 600, 1000 nodes.
- Number of games: 100 per tree size.

## Results
| Tree Size | Wins (Vanilla MCTS) | Wins (Modified MCTS) |
|-----------|----------------------|----------------------|
| 200       | 37                   | 63                   |
| 600       | 38                   | 62                   |
| 1000      | 45                   | 55                   |

## Analysis
- The modified MCTS bot consistently outperforms the vanilla MCTS bot across all tested tree sizes.
- The heuristic rollouts provide a significant advantage, leading to more wins for the modified bot.
- The performance gap is most noticeable at lower tree sizes and slightly decreases at higher tree sizes.
- See experiment2.pdf for detailed analysis.

## Conclusion
The modified MCTS bot with heuristic rollouts performs better than the vanilla MCTS bot. The heuristic improvements lead to a higher win rate, especially at smaller tree sizes, with the performance advantage slightly diminishing as the tree size increases.

