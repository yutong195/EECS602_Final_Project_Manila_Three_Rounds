'''
Author: SeekingAspdelus jz332@duke.edu
Date: 2022-12-10 02:57:03
LastEditors: SeekingAspdelus jz332@duke.edu
LastEditTime: 2022-12-10 03:30:13
FilePath: \AI_Game_Agent\benchmark_agent.py

Copyright (c) 2022 by SeekingAspdelus jz332@duke.edu, All Rights Reserved. 
'''
import numpy as np
from play import *
import util


class benchmark_agents(Player):
    def __init__(self, name, money, color, game):
        super().__init__(name, money, color, game)
        self.money = money
        self.verbose = False
        
    def set_verbose(self, verbose):
        self.verbose = verbose
    
    def convertAction(self, action):
        return self.action_val_dic[action.name]
    
    def my_turn(self):
        self.available_action_ls = self.get_action()
        if len(self.available_action_ls) == 1:
            self.available_action_ls[0].invest(self)
            return
        action = util.randomChoice(self.available_action_ls)
        self.money -= action.get_cost()
        action.invest(self)
        if self.verbose:
            print("{agent_name} invested in {investment_name}".format(agent_name=self.name, investment_name=action.name))
        