'''
Author: SeekingAspdelus jz332@duke.edu
LastEditors: SeekingAspdelus
Date: 2022-10-27 12:19:15
LastEditTime: 2022-12-16 00:02:45
FilePath: \AI_Game_Agent\play.py

All the method in this file is used to control the player's action.
method may be called in this file:
    get_behavior()
    get_name()
    get_money()
    get_color()
    invest()
    status()
'''



class Player():
    def __init__(self, name, money, color, game):
        self.name = name # player's name string
        self.money = money # in Peso int
        self.color = color # player's color
        self.behavior = [] #player's used behavior object
        self.game = game # game
        self.winrate = 0 # winrate

    def __str__(self):
        return f'{self.name} has {self.money} Peso, his/her color is {self.color}'

    def get_behavior(self):
        #What you have done in this game
        return self.behavior

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money

    def get_color(self):
        return self.color

    def invest(self, action):
        ''''
        update the available for this player now
        return whether the behavior is successful or not
        True: successful
        False: not successful
        '''
        self.get_action()
        if self.available_action == []:
            self.add_behavior(action)
            print('Sorry, but you have no available_action')
            self.skip()
            return True
        if action in self.available_action:
            self.add_behavior(action)
            self.money -= action.get_cost()
            action.invest(self)
            if action.name == 'Skip':
                print('You have skipped this term')
            else:
                print(f'You have succeeded in investing {action.name}')
            return True
        else:
            print('Invalid action, please specify an action from the list')
            return False

    def status(self):
        print(f'You are {self.name}, your color is {self.color}, you have {self.money} Peso')
        for i in self.behavior:
            print(f'You have invested in {i.name}')

    def my_turn(self):
        '''
        player's turn
        what to do:
        success or not
        accept the input from the player (human)
        '''
        print(f'Your turn, {self.name}')
        self.get_action()
        print('You can invest in:')
        for i in self.available_action:
            if i.name != 'Skip':
                print(f'{i.name} with cost {i.get_cost()}')
        """ for ship in self.game.ship_ls:
            print("{ship} now at position {position}".format(ship=ship.name, position=ship.position)) """
        print('You can also choose to skip this turn')
        print('Please specify the action you want to take')
        while True:
            action_input = input()
            action_next = ''
            for action in self.available_action:
                if action.name == action_input:
                    action_next = action
                    break
                else:
                    continue
            """ for k in range(len(self.game.action_ls)):
                if(self.game.action_ls[k].name == action_input):
                    action_next = self.game.action_ls[k]
                    break
                else:
                    continue """
            success_flag = self.invest(action_next)
            if success_flag:
                break
        return action_next

    def conclude(self):
        for i in self.behavior:
            investor_num = len(i.get_investors())
            self.profit(i.get_payback()/investor_num)
        print(f'You have {self.money} Peso now')

    #should not be called
    def set_money(self, money):
        self.money = money

    def add_behavior(self, behavior):
        self.behavior.append(behavior)

    def profit(self, money):
        self.money += money

    def skip(self):
        print('You have skipped your turn')

    def get_action(self):
        '''
        get the available action for the player
        objects in the list are investment objects
        available_action has available and affordable behavior in it
        available_action = [invest1, invest2, ...]
        '''
        self.available_action = []
        for i in self.game.port_ls:
            if i.get_availability():
                self.available_action.append(i)
        for i in self.game.shipyard_ls:
            if i.get_availability():
                self.available_action.append(i)
        for i in self.game.ship_ls:
            if i.get_availability():
                self.available_action.append(i)
        if self.game.skip.get_availability():
            self.available_action.append(self.game.skip)
        money = self.money
        for i in self.available_action:
            if i.get_cost() > money:
                self.available_action.remove(i)
        return self.available_action

    def next_game(self, game):
        self.set_money(30)
        self.game = game