from random import randint
from Cell import Cell

class Solver(Cell):
    def __init__(self):
        self.solver_active = False
        self.found = False

    # this is the opposite of numbers_image in a Cell class
    image = {u:i for i,u in Cell.numbers_image.items()}
    # one : 1

    # Activate the solver
    def Activate(self):
        if pygame.key.get_pressed()[pygame.K_1] or self.solver_active == True:
            return self.solver_active == True
        return False

    def Solve(self):
        self.solver_active = True
        if not self.found:
            self.Find_flood_fill() 
        else: 
            # for loop makes the algorithm look only at numbers. 
            if not Cell.no_of_bombs == Cell.marked:
                for ce in (ce for ce in Cell.cells_list if ce.img in Solver.image 
                            and Solver.Check_for_blocks(ce) > 0 and not ce.flagged):

                    if Solver.image[ce.img] == Solver.Check_for_flags(ce):
                        Solver.Discover_around(ce)
                    else:
                        if Solver.image[ce.img] == Solver.Check_for_blocks(ce):
                            Solver.Flag_everything(ce)
                        elif Solver.image[ce.img] == Solver.Check_for_flags(ce) + Solver.Check_for_blocks(ce):
                            Solver.Flag_everything(ce)
                
                # stop guessing at the end
                if Cell.no_of_bombs * 0.9 > Cell.marked:
                    Solver.Guess()
            else:
                self.solver_active = False
                print("Solved!")

    def Find_flood_fill(self):
        num = randint(0, Cell.no_of_cells - 1)
        Cell.cells_list[num].Cell_logic()
        self.found = True

    @staticmethod
    def Guess():
        """
        Guessing algorithm

        This counts bomb probability for every undiscovered block on board
        that is next to a number cell and makes predictions accordingly.
        """
        def probability(cell):
            P = 0
            for ce in (ce for ce in Cell.cells_list if ce.img in Solver.image):
                if ce.Check_tiny(cell):
                    P += Solver.image[ce.img] - Solver.Check_for_flags(ce) / Solver.Check_for_blocks(ce)
                    
            # this is to prevent the algo from picking corners
            return P if P != 0 else 10 

        cell_prob = {probability(block) : block for block in (block for block in Cell.cells_list 
                                                                if block.img == Cell.act["block"])}

        # picking an object with the lowest probability of bomb being in a cell
        if min(cell_prob) != None:
            return cell_prob[min(cell_prob)].Cell_logic()

    @staticmethod
    def Check_for_blocks(cell):
        """
        This func will check for blocks around
        parameter cell, returns int
        """
        blocks_around = 0
        for ce in (ce for ce in Cell.cells_list if not ce.discovered):
            if cell.Check_tiny(ce):
                blocks_around += 1
        return blocks_around

    @staticmethod
    def Discover_around(cell):
        """
        This func will "click" on every single undiscovered
        block around a parameter cell
        """
        for ce in (ce for ce in Cell.cells_list if ce.img == Cell.act["block"]):
            if cell.Check_tiny(ce):
                ce.Cell_logic()
   
    @staticmethod
    def Check_for_flags(cell):
        """
        This func will check for flags around
        parameter cell, returns int
        """
        flag_around = 0
        for ce in (ce for ce in Cell.cells_list if ce.img == Cell.act["flag"]):
            if cell.Check_tiny(ce):
                flag_around += 1
        return flag_around

    @staticmethod
    def Flag_everything(cell):
        """
        This func will "flag" every single undiscovered
        block around a parameter cell
        """
        for ce in (ce for ce in Cell.cells_list if not ce.discovered and not ce.flagged):
            if cell.Check_tiny(ce):
                ce.Flag()