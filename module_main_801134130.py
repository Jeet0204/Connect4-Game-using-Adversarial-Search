# UNC Charlotte
# ITCS 5010 - Applied AI - Spring 2020
# Homework 4
# Adversarial Search
# This module implements the main game flow and the strategies used in the game.
# For running this module 3 libraries need to be installed  : pygame, pygame_gui, and tkinter
# Student ID: 801134130


import random
import math
import functools
from collections import defaultdict
import pygame as pg
import pygame_gui as pgui
import sys, os
import module_interface_801134130
from tkinter import messagebox as mb
import tkinter as tk

cache = functools.lru_cache(10**6)

# List to keep the track of the visited nodes
explored = []

class Game:
    """A game is similar to a problem, but it has a terminal test instead of
    a goal test, and a utility for each terminal state. To create a game,
    subclass this class and implement `actions`, `result`, `is_terminal`,
    and `utility`. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError


class Control:
    """This class is the main class for executing the game as it calls the Interface class for creating the game interface.
    Also, In this class the main game is executed and there is function call to different AI algorithm
    self.State = module_interface_801134130.Interface()
        self.AI = Variable for representing the AI move
        self.User = Variable for representing the user move 
        self.Gameover = Variable for checking the game is over or not
        self.Clock = Variable for calculating time interval for updating different screens at differnet time itervals
        self.square_size = Variable for assigning a size to square
        self.cols = Variable for total number of column
        self.rows = variable for total number of rows
        self.move= self.User
        self.algo = Variable for choosing between two AI algorithm t the start of the game
        self.width = Variable for Calculating the width of the square todrop the piece
        self.height = Variable for Calculating the height of the square to drop the piece
        self.window = Variable for  Creating the main window for and integrated different screen in this window
        self.game_screen = Creating the screen for the main game board
        self.balldrop_screen = Creating the screen for the droping the piece by the user
        self.nextturn_screen = Creating the screen for displaying the Next Turn
        self.time_screen = Creating the screen for displaying the time taken by AI to play the move
        self.radius = Variable for calculating the radius of the circle
        self.logdata_screen = Creating the sccreen for displaying the dropdown
        self.screen = Creating the screen for displaying the logs
        self.manager = Manager is used for implementing the functionality like scrollbar and dropdown
        self.visited = This keeps track of the selected moves
        self.winner = Variable to display the popup for the winner
        self.game_started = When the value of this variable is 'On' it starts the game
        self.log = This variable maintains the log of the explored state
        """

    def __init__(self):
        self.State = module_interface_801134130.Interface()
        self.AI = 'X'
        self.User = 'O'
        self.Gameover = False
        self.Clock = pg.time.Clock()
        self.square_size = 75
        self.cols = 7
        self.rows = 6
        self.move= self.User
        self.algo = 'minimax_search'
        self.width = self.cols * self.square_size
        self.height = (self.rows + 1) * self.square_size
        self.window = pg.display.set_mode((800, 600))
        self.game_screen = pg.Surface((525, 525))
        self.balldrop_screen = pg.Surface((525, 75))
        self.nextturn_screen = pg.Surface((275,75))
        self.time_screen = pg.Surface((275,75))
        self.radius = int((self.square_size / 2) - 5)
        self.logdata_screen = pg.Surface((275, 225))
        self.screen = pg.Surface((275,225))
        self.manager = pgui.UIManager((275, 600))
        self.visited = {}
        self.winner = 'X'
        self.game_started = 'Off'
        self.log = ''


    def play_game(self,game, strategies: dict, verbose=False):
        """Play a turn-taking game. `strategies` is a {player_name: function} dict,
        where function(state, game) is used to get the player's move."""
        
        #Initializing the game state and the explored nodes
        state = game.initial
        nodes = '0'

        #Declaration of dropbox select to select the algorithm before the sart of the game
        self.ai_algo = pgui.elements.UIDropDownMenu(options_list=["minimax_search", "alphabeta_search"],
                                                    starting_option="minimax_search",
                                                    relative_rect=pg.Rect((20, 10), (200, 65)),
                                                    manager=self.manager)
        self.logdata_screen.fill((10, 20, 30))
        
        #Function call for drawing different screen
        self.State.window_surfaces()
        
        #Function call for drawing the game board
        self.State.draw_board(self.visited)
        self.Clock = pg.time.Clock()

        #Loop to check if the game is over or not
        while not self.Gameover:

            #If-Else for checking terminal state is reached then display the pop up of the winner
            if not game.is_terminal(state):

                self.time_delta = self.Clock.tick(60) / 1000.0

                # Creating Game Buttons
                game_status_start = self.State.game_button("New Game", 340, 130, 10, 40, (19, 252, 7), (26, 171, 18), "Start")
                game_status_restart =  self.State.game_button("Restart", 495, 120, 10, 40, (251, 254, 6), (230, 233, 19), "Restart")
                self.State.game_button("Exit", 650, 120, 10, 40, (252, 70, 45), (213, 46, 23), "Exit")

                # Creating Game Surface
                self.balldrop_screen.fill((0, 0, 0))

                # Assigning a move
                player = state.to_move

                #Check if the game is started or not, If started then display the next turn
                if self.game_started=='On':
                    self.nextturn_screen.fill((10, 20, 30))
                    self.window.blit(self.nextturn_screen, (0, 225))
                    self.State.display_turn(player)

                # If condition for restart or new game. All the variables are re initialized
                if game_status_restart=='restart' or game_status_start=='start':
                    self.visited = {}
                    state = game.initial
                    self.State.draw_board(self.visited)
                    nodes = '0'


                #Loop condition for the checking the USer events
                for event in pg.event.get():

                    #Checking is ESC key or close window is pressed or not for quitting the game
                    self.keys = pg.key.get_pressed()
                    if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                        self.Gameover = True

                    # If statement for moving the ball from right to left on the game screen to insert the ball in a particular column
                    if event.type == pg.MOUSEMOTION and self.game_started=='On':
                        pg.draw.rect(self.game_screen, (0, 0, 0), (0, 0, self.width, self.square_size))
                        pos = pg.mouse.get_pos()
                        # print(pos[0], pos[1])
                        if 800 > pos[0] > 275 and 600 > pos[1] > 75 and self.move == 'O':
                            pg.draw.circle(self.balldrop_screen, (255, 255, 0), (pos[0] - 275, int(self.square_size / 2)),
                                           self.radius)
                        self.window.blit(self.balldrop_screen, (275, 75))

                    # If Mouse button is pressed and its users turn then checks the possible move and insert the ball in a selected column 
                    # and updates the board.
                    if event.type == pg.MOUSEBUTTONDOWN and event.pos[1]>75:
                        if player == self.User and (game_status_start=='start' or self.game_started == 'On'):
                            self.game_started = 'On'
                            pos = pg.mouse.get_pos()
                            col = math.floor((pos[0]-275) / self.square_size)

                            if col<0:
                                continue

                            for (x,y) in list(game.actions(state)):
                                if x==col:
                                    move = (x,y)

                            state = game.result(state, move)
                            key = 'O'

                            self.visited.setdefault(key, []).append(move)
                            self.State.draw_board(self.visited)

                    #At the start of the game user can select the AI algorithm from the dropdown
                    if event.type == pg.USEREVENT:
                        if self.game_started=='On':
                            self.State.showerrors()
                        if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED:
                            if event.ui_element == self.ai_algo:
                                print("Selected option:", event.text)
                                self.algo = event.text
                                return True

                    self.manager.process_events(event)

                #In this piece of code AI takes the move, displays the time taken by AI for selecting the move and updates the log window.
                if player == self.AI and (game_status_start=='start' or self.game_started == 'On'):
                    count = 0
                    if count==0:
                        self.State.display_turn(player)
                        count=1
                    self.game_started = 'On'
                    start = pg.time.get_ticks()
                    move = strategies[player](game, state)
                    end = pg.time.get_ticks()
                    self.AI_time = end - start

                    nodes = nodes + '\n Total number of explored nodes: '+str(len(explored))
                    
                    logs = pgui.windows.ui_message_window.UIMessageWindow(message_window_rect=pg.Rect((0, 375), (270, 220)),
                                                                   message_title="Log Window",
                                                                   html_message=nodes,
                                                                   manager=self.manager)
                    explored.clear()
                    self.time_screen.fill((10, 20, 30))
                    self.window.blit(self.time_screen,(0,300))
                    self.State.display_time(self.AI_time/1000,self.AI_time/60000)
                    pg.display.update()

                    state = game.result(state, move)

                    key = 'X'
                    self.visited.setdefault(key,[]).append(move)
                    self.State.draw_board(self.visited)


                self.manager.update(self.time_delta)
                self.manager.draw_ui(self.window)
                pg.display.update()


            #Once the terminal state is reached, the execution goes to this else part and it pops up the window with the winner name
            else:
                if player=='X':
                    self.State.showmessage('AI Won the Game')
                    pg.quit()
                    quit()
                else:
                    self.State.showmessage('User Won the Game')
                    pg.quit()
                    quit()

infinity = math.inf


class TicTacToe(Game):
    """Play TicTacToe on an `height` by `width` board, needing `k` in a row to win.
    'X' plays first against 'O'."""

    def __init__(self, height=3, width=3, k=3):
        self.k = k  # k in a row
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        print('square:',self.squares)
        self.initial = Board(height=height, width=width, to_move='X', utility=0)

    def actions(self, board):
        """Legal moves are any square not yet taken."""
        return self.squares - set(board)

    def result(self, board, square):
        """Place a marker for current player on square."""
        player = board.to_move
        board = board.new({square: player}, to_move=('O' if player == 'X' else 'X'))
        win = k_in_row(board, player, square, self.k)
        board.utility = (0 if not win else +1 if player == 'X' else -1)
        return board

    def utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return board.utility if player == 'X' else -board.utility

    def is_terminal(self, board):
        """A board is a terminal state if it is won or there are no empty squares."""
        return board.utility != 0 or len(self.squares) == len(board)

    def display(self, board): print(board)


def k_in_row(board, player, square, k):
    """True if player has k pieces in a line through square."""

    def in_row(x, y, dx, dy): return 0 if board[x, y] != player else 1 + in_row(x + dx, y + dy, dx, dy)

    return any(in_row(*square, dx, dy) + in_row(*square, -dx, -dy) - 1 >= k
               for (dx, dy) in ((0, 1), (1, 0), (1, 1), (1, -1)))

class Board(defaultdict):
    """A board has the player to move, a cached utility value,
    and a dict of {(x, y): player} entries, where player is 'X' or 'O'."""
    empty = '.'
    off = '#'

    def __init__(self, width=7, height=6, to_move=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)

    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))

        return '\n'.join(map(row, range(self.height))) + '\n'


def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]

class ConnectFour(TicTacToe):

    def __init__(self): super().__init__(width=7, height=6, k=4)

    def actions(self, board):
        """In each column you can play only the lowest empty square in the column."""
        return {(x, y) for (x, y) in self.squares - set(board)
                if y == board.height - 1 or (x, y + 1) in board}

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d


#Since expanding the game tree is not feasible minimax is implemented with depth 3.
def minimax_search(game, state, cutoff=cutoff_depth(3), h=lambda s, p: 0):
    """Search game tree to determine best move; return (value, move) pair."""
    player = state.to_move
    def max_value(state, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None

        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), depth + 1)
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        explored.append(len(game.actions(state)))
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), depth + 1)
            if v2 < v:
                v, move = v2, a
        return v, move
    return max_value(state, 0)

#In alphabeta search also since expanding of whole tree is not possible, it can go to maximum of depth 6.
def alphabeta_search(game, state, cutoff=cutoff_depth(6), h=lambda s, p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None
        explored.append(len(game.actions(state)))
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)


def main():
    """Initialize the display and create an instance of Control."""
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption("Connect4 Game")
    pg.display.set_mode((800, 600))
    RunIt = Control()
    connect4 = ConnectFour()
    game_play = RunIt.play_game(connect4, dict(X=player(eval(RunIt.algo))), verbose=True)
    while game_play==True:
        RunIt.play_game(connect4, dict(X=player(eval(RunIt.algo))), verbose=True)
    pg.quit()
    pg.quit();
    sys.exit()

if __name__ == "__main__":
    main()


