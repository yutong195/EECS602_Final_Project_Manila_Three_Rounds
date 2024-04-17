'''
Author: SeekingAspdelus jz332@duke.edu
Date: 2022-12-10 02:57:03
LastEditors: Tianle Zhu
LastEditTime: 2022-12-16 20:33:40
FilePath: \AI_Game_Agent\Manila.py

Copyright (c) 2022 by SeekingAspdelus jz332@duke.edu, All Rights Reserved. 
'''
import matplotlib.pyplot as plt
import numpy as np
import random
import game
import play
import time
import agents
import dqn

def main(args):
    # create a game
    g = game.Game(args.verbose)
    # create AI players
    if args.mode == 'Q_learning':
        player1 = agents.QlearningAgent("Player1", 30, None, g)
        player2 = agents.QlearningAgent("Player2", 30, None, g)
        player3 = agents.QlearningAgent("Player3", 30, None, g)
    elif args.mode == 'DQN':
        player1 = dqn.DQNAgent("Player1", 30, None, g)
        player2 = dqn.DQNAgent("Player2", 30, None, g)
        player3 = dqn.DQNAgent("Player3", 30, None, g)
    player1.set_factor(0.3)
    player1.set_greedy_factor(10)
    player2.set_factor(1)
    player2.set_greedy_factor(1)
    player3.set_factor(1.8)
    player3.set_greedy_factor(0.1)
    # add human players to the game
    if args.AI_num == 0:
        player1 = play.Player("Player1", 30, None, g)
        player2 = play.Player("Player2", 30, None, g)
        player3 = play.Player("Player3", 30, None, g)
    elif args.AI_num == 1:
        player1 = play.Player("Player1", 30, None, g)
        player2 = play.Player("Player2", 30, None, g)
    elif args.AI_num == 2:
        player1 = play.Player("Player1", 30, None, g)
    player_ls = [player1, player2, player3]
    # shuffle the player list
    random.shuffle(player_ls)

    g.add_player(player_ls)

    # start the train
    print('------ Training ------')
    for epoch in range(args.epoch):
        t_start = time.time()
        g.start()
        if args.verbose:
            print("Player1's final money:", int(player_ls[0].money))
            print("Player2's final money:", int(player_ls[1].money))
            print("Player3's final money:", int(player_ls[2].money))
        money_ls = [player_ls[0].money, player_ls[1].money, player_ls[2].money]
        win_idx = money_ls.index(max(money_ls))
        player_ls[win_idx].winrate += 1
        # terminal round, update the network
        if player1.train_flag:
            for idx, player in enumerate(player_ls):
                last_index = (player.memoryCounter - 1 + player.memory_size) % player.memory_size
                player.terminal_memory[last_index] = 1
                player.reward_memory[last_index] = player.money / max(money_ls)
                # if idx == win_idx:
                #     player.reward_memory[last_index] = 1
                # else:
                #     player.reward_memory[last_index] = -1
                player.learn()

        g = game.Game(args.verbose)

        #shuffle the player list
        random.shuffle(player_ls)
        for player in player_ls:
            player.next_game(g)
        g.add_player(player_ls)
        t_end = time.time()
        print('Epoch {:02d} | Time: {:.4f}'.format(epoch+1, t_end-t_start))
    print(  'Player1 train winrate: {:.2f}%'.format(player1.winrate/args.epoch*100),
            'Player2 train winrate: {:.2f}%'.format(player2.winrate/args.epoch*100),
            'Player3 train winrate: {:.2f}%'.format(player3.winrate/args.epoch*100), sep='\t')
    
    
    # plot loss for DQN agents
    if args.mode == "DQN":
        loss1 = player1.loss_ls
        loss2 = player2.loss_ls
        loss3 = player3.loss_ls

        player1.set_train_flag(False)
        player2.set_train_flag(False)
        player3.set_train_flag(False)
        wins = [0] * 3
        player_ls = [player1, player2, player3]
        g = game.Game(args.verbose)
        g.add_player(player_ls)
        for epoch in range(args.epoch//2):
            g.start()
            if args.verbose:
                print("Player1's final money:", int(player_ls[0].money))
                print("Player2's final money:", int(player_ls[1].money))
                print("Player3's final money:", int(player_ls[2].money))
            money_ls = [player_ls[0].money, player_ls[1].money, player_ls[2].money]
            wins[money_ls.index(max(money_ls))] += 1
            g = game.Game(args.verbose)
            for player in player_ls:
                player.next_game(g)
            g.add_player(player_ls)
        print(  'Player1 eval winrate: {:.2f}%'.format(wins[0]/args.epoch*200),
            'Player2 eval winrate: {:.2f}%'.format(wins[1]/args.epoch*200),
            'Player3 eval winrate: {:.2f}%'.format(wins[2]/args.epoch*200), sep='\t')


        plt.figure(figsize=(24,9))
        plt.subplot(131)
        plt.plot(np.arange(len(loss1)),loss1)
        plt.title("loss of player1")
        plt.subplot(132)
        plt.plot(np.arange(len(loss2)),loss2)
        plt.title("loss of player2")
        plt.subplot(133)
        plt.plot(np.arange(len(loss3)),loss3)
        plt.title("loss of player3")
        plt.show()
    
    # save the qtable
    if args.mode == 'Q_learning':
        print('------ Saving Q_learning------')
        player1.saveQtable("qtable_aggressive.json")
        player2.saveQtable("qtable_normal.json")
        player3.saveQtable("qtable_conservative.json")
    elif args.mode == 'DQN':
        print('------ Saving DQN------')
        player1.saveWeights("dqn_aggressive.pth")
        player2.saveWeights("dqn_normal.pth")
        player3.saveWeights("dqn_conservative.pth")
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='GNN')

    # Player options
    parser.add_argument('--AI_num', type=int, default=3, help = "number of AI players (0-3)")

    # Print options
    parser.add_argument('--verbose',  type=bool, default=False, help = "whether to print the game process")

    # Game options
    parser.add_argument('--epoch', type=int, default=100, help = "number of games")
    parser.add_argument('--mode', type = str, default='Q_learning', help = "use what method")
    args = parser.parse_args()

    print(args)
    main(args)