import matplotlib.pyplot as plt
import numpy as np
import random
import game
import dqn

g = game.Game(verbose=False)
player1 = dqn.DQNAgent("Player1", 30, None, g)
player2 = dqn.DQNAgent("Player2", 30, None, g)
player3 = dqn.DQNAgent("Player3", 30, None, g)
player1.set_factor(0.3)
player1.set_greedy_factor(10)
player2.set_factor(1)
player2.set_greedy_factor(1)
player3.set_factor(1.8)
player3.set_greedy_factor(0.1)

player1.loadWeights("dqn_aggressive.pth")
player2.loadWeights("dqn_normal.pth")
player3.loadWeights("dqn_conservative.pth")
player1.set_train_flag(False)
player2.set_train_flag(False)
player3.set_train_flag(False)
wins = [0] * 3
player_ls = [player1, player2, player3]
random.shuffle(player_ls)
g.add_player(player_ls)
for epoch in range(1000):
    g.start()
    # print("Player1's final money:", int(player_ls[0].money))
    # print("Player2's final money:", int(player_ls[1].money))
    # print("Player3's final money:", int(player_ls[2].money))
    money_ls = [player_ls[0].money, player_ls[1].money, player_ls[2].money]
    win_idx = money_ls.index(max(money_ls))
    player_ls[win_idx].winrate += 1
    g = game.Game(verbose=False)
    random.shuffle(player_ls)
    for player in player_ls:
        player.next_game(g)
    g.add_player(player_ls)
print(  '{} eval winrate: {:.2f}%'.format(player_ls[0].name, player_ls[0].winrate/1000*100),
            '{} eval winrate: {:.2f}%'.format(player_ls[1].name, player_ls[1].winrate/1000*100),
            '{} eval winrate: {:.2f}%'.format(player_ls[2].name, player_ls[2].winrate/1000*100), sep='\t')