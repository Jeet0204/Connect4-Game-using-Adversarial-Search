# UNC Charlotte
# ITCS 5010 - Applied AI - Spring 2020
# Homework 4
# Adversarial Search
# This module implements the Interface of the game. It creates different screens in the window, buttons, text, scrollbar and popup window.
# Student ID: 801134130


import pygame as pg
import numpy as np
import random
import pygame_gui as pgui
import module_main_801134130
import tkinter as tk
from tkinter import messagebox as mb


class Interface(object):
    """This class implements the GUI for user for iteracting with the game """
    def __init__(self):
        self.window = pg.display.set_mode((800, 600))
        self.square_size = 75
        self.radius = int((self.square_size / 2) - 5)
        self.game_screen = pg.Surface((525, 525))
        self.balldrop_screen = pg.Surface((525, 75))
        self.time_screen = pg.Surface((275,75))
        self.nextturn_screen = pg.Surface((275,75))
        self.logdata_screen = pg.Surface((275, 225))
        self.manager = pgui.UIManager((275, 600))
        self.rows = 6
        self.cols = 7

    # This function draws the main game board in the window in game screen
    def draw_board(self, visited):
        for col in range(self.cols):
            for row in range(self.rows):
                pg.draw.rect(self.game_screen, (0, 0, 255),
                             (col * self.square_size, row * self.square_size + self.square_size, self.square_size,
                              self.square_size))
                pg.draw.circle(self.game_screen, (0, 0, 0), (
                    int(col * self.square_size + self.square_size / 2),
                    int(row * self.square_size + self.square_size + self.square_size / 2)),
                               self.radius)
        for key in visited:
            if (key == 'X'):
                vals = visited.get(key)
                for (c, r) in vals:
                    pg.draw.circle(self.game_screen, (255, 0, 0), (int(c * self.square_size + self.square_size / 2),
                                                                    int(r * self.square_size + self.square_size / 2) + 75),
                                                                    self.radius)
            elif (key == 'O'):
                vals = visited.get(key)
                for (c, r) in vals:
                    pg.draw.circle(self.game_screen, (255, 255, 0), (int(c * self.square_size + self.square_size / 2),
                                                                      int(r * self.square_size + self.square_size / 2) + 75),
                                                                        self.radius)

        self.window.blit(self.game_screen, (275, 75))
        pg.display.update()
    def dropdown(self):
        self.ai_algo = pgui.elements.UIDropDownMenu(options_list=["minimax_search", "alphabeta_search"],
                                                    starting_option="minimax_search",
                                                    relative_rect=pg.Rect((20, 10), (200, 65)),
                                                    manager=self.manager)

    # This function is used for updating the text
    def fetch_text(self, text, font, clr):
        textSurface = font.render(text, True, clr)
        return textSurface, textSurface.get_rect()

    # This function displays the current turn of the player
    def display_turn(self, move):
        if move == 'O':
            text_type = pg.font.Font("freesansbold.ttf", 20)
            textSurf, textRect = self.fetch_text("User's Turn", text_type, (225, 225, 205))
            textRect.center = (275 / 2, 260)
            return self.window.blit(textSurf, textRect)
        elif move == 'X':
            text_type = pg.font.Font("freesansbold.ttf", 20)
            textSurf, textRect = self.fetch_text("AI's turn", text_type, (225, 225, 205))
            textRect.center = (275 / 2, 260)
            return self.window.blit(textSurf, textRect)

    # This is the popup window which opens when any player wins the game
    def showmessage(self,msg):
        root = tk.Tk()
        root.withdraw()
        mb.showinfo("Result", msg)
        root.destroy()

    # This function popups the error window if user try to change search algorithm ib between the game
    def showerrors(self):
        root = tk.Tk()
        root.withdraw()
        mb.showerror("Error", "You cannot change the in between the game, you can only select algorithm at the start of the game" )
        root.destroy()

    #This function displays the time taken by Ai to play the move
    def display_time(self, sec, min):
        text_type = pg.font.Font("freesansbold.ttf", 15)
        textSurf, textRect = self.fetch_text('Time taken by AI: ' + str(round(sec, 5)) + ' sec', text_type,
                                             (225, 225, 205))
        textRect.center = (275 / 2, 320)
        self.window.blit(textSurf, textRect)
        text_type = pg.font.Font("freesansbold.ttf", 15)
        textSurf, textRect = self.fetch_text('Time taken by AI: ' + str(round(min, 5)) + ' min', text_type,
                                             (225, 225, 205))
        textRect.center = (275 / 2, 350)
        self.window.blit(textSurf, textRect)

    # Initializes all the screen of the game in the main window
    def window_surfaces(self):
        self.time_screen.fill((10, 20, 30))
        self.window.blit(self.time_screen, (0, 300))

        self.nextturn_screen.fill((10, 20, 30))
        self.window.blit(self.nextturn_screen, (0, 225))

        self.logdata_screen.fill((10, 20, 30))
        self.window.blit(self.logdata_screen, (0, 0))
        

        self.balldrop_screen.fill((0, 0, 0))
        self.window.blit(self.balldrop_screen, (275, 75))

        self.game_screen.fill((0, 0, 0))
        self.window.blit(self.game_screen, (275, 75))
        pg.display.update()


    # This function is used for creating the buttons in the game
    def game_button(self, msg, x, w, y, h, on, off, action=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pg.draw.rect(self.window, on, (x, y, w, h))
            if click[0] == 1 and action != None:
                if action == 'Start':
                    return 'start'
                elif action == 'Restart':
                    return 'restart'
                elif action == 'Exit':
                    pg.quit()
                    quit()
        else:
            pg.draw.rect(self.window, off, (x, y, w, h))

        text_type = pg.font.Font("freesansbold.ttf", 25)
        textSurf, textRect = self.fetch_text(msg, text_type, (0, 0, 0))
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.window.blit(textSurf, textRect)
