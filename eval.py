import matplotlib.pyplot as plt
import numpy as np
    
import game
import dqn

g = game.Game(verbose=False)
player1 = dqn.DQNAgent("Player1", 30, None, g)
player2 = dqn.DQNAgent("Player2", 30, None, g)
player3 = dqn.DQNAgent("Player3", 30, None, g)
# player1.set_factor(1)
# player2.set_factor(1)
# player3.set_factor(1)

player1.loadWeights("eval/dqn_normal_reward_0.pth")
player2.loadWeights("eval/dqn_normal_reward_0.pth")
player3.loadWeights("eval/dqn_normal_reward_0.pth")
player1.set_train_flag(False)
player2.set_train_flag(False)
player3.set_train_flag(False)
wins = [0] * 3
player_ls = [player1, player2, player3]
g.add_player(player_ls)
for epoch in range(1000):
    g.start()
    # print("Player1's final money:", int(player_ls[0].money))
    # print("Player2's final money:", int(player_ls[1].money))
    # print("Player3's final money:", int(player_ls[2].money))
    money_ls = [player_ls[0].money, player_ls[1].money, player_ls[2].money]
    wins[money_ls.index(max(money_ls))] += 1
    g = game.Game(verbose=False)
    for player in player_ls:
        player.next_game(g)
    g.add_player(player_ls)
print(  'Player1 eval winrate: {:.2f}%'.format(wins[0]/1000*100),
    'Player2 eval winrate: {:.2f}%'.format(wins[1]/1000*100),
    'Player3 eval winrate: {:.2f}%'.format(wins[2]/1000*100), sep='\t')