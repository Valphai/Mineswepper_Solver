import pygame
import os
from numpy.random import choice

directory = "{}/Textures/".format(os.getcwd())
action_dir = "{}Action".format(directory)
nums_dir = "{}Numbers".format(directory)

WIDTH = 600
HEIGHT = 300

dx = 16 # small distance for cell clicking

class Cell:
    def __init__(self, pos_x, pos_y, inside="block", discovered = False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.inside = inside # hidden inside of the cell
        self.discovered = discovered
        self.img = Cell.act["block"]
        self.flagged = False

    # numbers
    numbers_image = {i:pygame.image.load(os.path.join(nums_dir, u)) 
                        for i, u in enumerate(os.listdir(nums_dir),1)}

    # blocks other than numbers
    act = {u[:-4] : pygame.image.load(os.path.join(action_dir, u)) 
                        for u in os.listdir(action_dir)}

    small_area = [(0,-dx), (-dx,-dx), (-dx,0), (-dx,dx), 
                    (0,dx), (dx,dx), (dx,0), (dx,-dx)]
    
    spawn_probability = [1/6, 5/6]
    marked = 0 # the amount of flags
    no_of_cells = 0
    no_of_bombs = 0
    cells_list = []
    first_click = True
    lost = False

    def draw(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    # randomize the inside of the cell
    def Assign_bombs(self):
        """
        The rule in mineswepper is that the first click has to always
        be floodfill. 
        The idea is that this func will be called after the 1st click
        """
        for ce in Cell.cells_list:
            if not (ce.pos_x, ce.pos_y) == (self.pos_x, self.pos_y):
                ce.inside = choice(["bomb", "block"],p=Cell.spawn_probability)
                if ce.inside == "bomb":
                    Cell.no_of_bombs += 1

    @classmethod
    def Initialize_board(cls):
        for i in range(0, WIDTH - 100): # 100 and 20 is for padding
            for j in range(0, HEIGHT - 20):
                if i % dx == 0 and i != 0:
                    if j % dx == 0 and j != 0:
                        ce = Cell(i, j)
                        Cell.cells_list.append(ce)
                        Cell.no_of_cells += 1

    def Flag(self):
        if not self.discovered:
            if not self.flagged:
                self.img = Cell.act["flag"]
                Cell.marked += 1
                self.flagged = True
            elif self.flagged:
                self.img = Cell.act["block"]
                Cell.marked -= 1
                self.flagged = False

    def Cell_logic(self):
        """
        The main logic of the script. This is where the script looks after
        a click on the cell.
        """
        if not Cell.first_click:
            if self.inside == "bomb":
                for ce in (ce for ce in Cell.cells_list if ce.inside == "bomb" and not ce.flagged):
                    ce.img = Cell.act["bomb"]
                self.img = Cell.act["red_bomb"]
                Cell.lost = True
            else:
                self.Look_around()
        else: # first time
            self.Assign_bombs()
            self.Flood_fill()
            self.Look_around()
            Cell.first_click = False

    def Check_tiny(self, ce):
        """
        The idea here is to point to 8 cells that are around an instance.
        """
        for dx, dy in self.small_area:
            if (self.pos_x + dx, self.pos_y + dy) == (ce.pos_x, ce.pos_y):
                return True

    # Here is what happends after a click on a cell if it's not a bomb
    def Look_around(self):
        """
        This counts the amount of bombs and decides afterwards what
        to do with an instance cell
        """
        self.discovered = True
        bombs_around = 0
        for ce in Cell.cells_list:
            if self.Check_tiny(ce) and ce.inside == "bomb":
                bombs_around += 1

        if bombs_around == 0:
            self.Flood_fill()
        else:
            self.img = Cell.numbers_image[bombs_around]
    
    def Flood_fill(self):
        for ce in (ce for ce in Cell.cells_list if self.Check_tiny(ce) and ce.inside != "bomb" and not ce.discovered):
            self.img = Cell.act["discov"]
            ce.img = Cell.act["discov"]
            ce.discovered = True
            ce.Look_around()