import matplotlib.pyplot as plt
import numpy as np
import random
import game
import play
import time
import agents
import dqn
import os
random.seed(42)
'''
 python DQN_hier.py --mode DQN --AI_num 3 --epoch 2000 --verbose False
'''

def sample_files(directory, sample_size=2):
    # Filter and list only files that end with '.pth'
    files = [file for file in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, file)) and file.endswith('.pth')]
    # Randomly sample 'sample_size' files from the list, ensuring there are enough files

    sampled_files = []
    for i in range(sample_size):
        sampled_files.append(random.choice(files))

    return sampled_files


def generate_player(player_path, player_name, g:game.Game):
    player = dqn.DQNAgent(player_name, 30, None, g)
    params = os.path.basename(player_path).strip('.pth').split('_')
    player.set_gamma(float(params[0]))
    player.set_update_target_every(float(params[1]))
    player.set_greedy_factor(float(params[2]))
    player.set_random(params[3]=='True')
    player.loadWeights(player_path)
    return player



def main(args):
    # CHANGE THE HYPERPARAMETERS HERE
    gamma = 0.1
    update_target_every = 40
    greedy_factor = 0.5
    random_ = False

    # Usage example
    directory_path = 'Players'
    save_path = 'Players1'

    g = game.Game(args.verbose)
    # create AI players
    if args.mode == 'Q_learning':
        player1 = agents.QlearningAgent("Player1", 30, None, g)
        player2 = agents.QlearningAgent("Player2", 30, None, g)
        player3 = agents.QlearningAgent("Player3", 30, None, g)
    elif args.mode == 'DQN':
        player1 = dqn.DQNAgent("Train Player", 30, None, g)
        # player2 = dqn.DQNAgent("Player2", 30, None, g)
        # player3 = dqn.DQNAgent("Player3", 30, None, g)
        player1.set_gamma(gamma)
        player1.set_update_target_every(update_target_every)
        player1.set_greedy_factor(greedy_factor)
        player1.set_random(random_)
        player1.set_train_flag(True)

    player2_file, player3_file = sample_files(directory_path, 2)
    player2 = generate_player(os.path.join(directory_path, player2_file), "Player2", g)
    player3 = generate_player(os.path.join(directory_path, player3_file), "Player3", g)
    player2.set_train_flag(False)
    player3.set_train_flag(False)

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
            print(f"{player_ls[0].name} final money:", int(player_ls[0].money))
            print(f"{player_ls[1].name} final money:", int(player_ls[1].money))
            print(f"{player_ls[2].name} final money:", int(player_ls[2].money))
        money_ls = [player_ls[0].money, player_ls[1].money, player_ls[2].money]
        # win_idx = money_ls.index(max(money_ls))
        # player_ls[win_idx].winrate += 1
        # terminal round, update the network

        for idx, player in enumerate(player_ls):
            if player.train_flag:
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

        player2_file, player3_file = sample_files(directory_path, 2)
        player2 = generate_player(os.path.join(directory_path, player2_file), "Player2", g)
        player3 = generate_player(os.path.join(directory_path, player3_file), "Player3", g)
        player2.set_train_flag(False)
        player3.set_train_flag(False)
        player_ls = [player1, player2, player3]

        random.shuffle(player_ls)
        for player in player_ls:
            player.next_game(g)
        g.add_player(player_ls)
        t_end = time.time()
    #     print('Epoch {:02d} | Time: {:.4f}'.format(epoch+1, t_end-t_start))
    # print(  'Player1 train winrate: {:.2f}%'.format(player1.winrate/args.epoch*100),
    #         'Player2 train winrate: {:.2f}%'.format(player2.winrate/args.epoch*100),
    #         'Player3 train winrate: {:.2f}%'.format(player3.winrate/args.epoch*100), sep='\t')
    

    print('------ Saving DQN------')
    player1_filename = '_'.join([str(player1.gamma), str(player1.update_target_every), str(player1.greedy_factor), str(player1.random)])
    player2_filename = '_'.join([str(player2.gamma), str(player2.update_target_every), str(player2.greedy_factor), str(player2.random)])
    player3_filename = '_'.join([str(player3.gamma), str(player3.update_target_every), str(player3.greedy_factor), str(player3.random)])
    if player1.train_flag:
        print(f"Saving player1 to {os.path.join(save_path, player1_filename)}")
        player1.saveWeights(os.path.join(save_path, player1_filename) + ".pth")
    if player2.train_flag:
        player2.saveWeights(os.path.join(save_path, player2_filename)+".pth")
    if player3.train_flag:
        player3.saveWeights(os.path.join(save_path, player3_filename)+".pth")
    
    # plot loss for DQN agents
    if args.mode == "DQN":
        loss1 = player1.loss_ls

        player1.set_train_flag(False)

        plt.figure(figsize=(24,9))
        plt.plot(np.arange(len(loss1)),loss1)
        plt.title("loss of player1")
        plt.show()
    
    

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