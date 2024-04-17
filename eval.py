import matplotlib.pyplot as plt
import numpy as np
import random
import game
import dqn

import os
import random
random.seed(42)


def run_test(test_path, agent1, agent2):
    g = game.Game(verbose=False)
    player1 = dqn.DQNAgent("Eval_Player", 30, None, g)
    player2 = dqn.DQNAgent("Player2", 30, None, g)
    player3 = dqn.DQNAgent("Player3", 30, None, g)

    player1.loadWeights(test_path)
    player2.loadWeights(agent1)
    player3.loadWeights(agent2)

    params1 = os.path.basename(test_path).strip('.pth').split('_')
    player1.set_gamma(float(params1[0]))
    player1.set_update_target_every(float(params1[1]))
    player1.set_greedy_factor(float(params1[2]))
    player1.set_random(params1[3]=='True')
    
    params2 = os.path.basename(agent1).strip('.pth').split('_')
    player2.set_gamma(float(params2[0]))
    player2.set_update_target_every(float(params2[1]))
    player2.set_greedy_factor(float(params2[2]))
    player2.set_random(params2[3]=='True')

    params3 = os.path.basename(agent2).strip('.pth').split('_')
    player3.set_gamma(float(params3[0]))
    player3.set_update_target_every(float(params3[1]))
    player3.set_greedy_factor(float(params3[2]))
    player3.set_random(params3[3]=='True')
    
    player1.set_train_flag(False)
    player2.set_train_flag(False)
    player3.set_train_flag(False)
    
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
    
    for idx, player in enumerate(player_ls):
        if player.name == "Eval_Player":
            return player.winrate/1000*100


def sample_files(directory, sample_size=2):
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    
    # Randomly sample 'sample_size' files from the list
    sampled_files = random.sample(files, sample_size)
    return sampled_files

# Usage example
directory_path = 'Players'
test_player = "0.1_1_0.1_False.pth"

win_rate_list = []

for i in range(20):
    sampled_files = sample_files(directory_path)
    print(sampled_files)
    win_rate = run_test(test_path=os.path.join(directory_path, test_player), 
                        agent1=os.path.join(directory_path, sampled_files[0]), 
                        agent2=os.path.join(directory_path, sampled_files[1]))
    win_rate_list.append(win_rate)

print(win_rate_list)
print("Average win rate: ", sum(win_rate_list)/len(win_rate_list))
