import pygame
import os
from Cell import Cell, WIDTH, HEIGHT, dx
from Solver import Solver

pygame.font.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
fontSize = 13
WHITE = (255, 255, 255)

def main():
    run = True

    Cell.Initialize_board()
    
    main_font = pygame.font.SysFont("arial", fontSize)

    def update_window():
        win.fill((0, 0, 0))
        bombs_text = main_font.render(f"Marked = {Cell.marked}/{Cell.no_of_bombs}", 1, WHITE)
        
        win.blit(bombs_text, (WIDTH - bombs_text.get_width() -5, HEIGHT - bombs_text.get_height() - 5))

        for ce in Cell.cells_list:
            ce.draw(win)

        pygame.display.update()
        
    while run:
        update_window()

        if pygame.key.get_pressed()[pygame.K_1] or solver.solver_active and not Cell.lost:
            solver.Solve()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        else:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not Cell.lost:
                    # if left mouse button pressed
                    if event.button == 1:
                        for ce in Cell.cells_list:
                            if ce.pos_x < event.pos[0] < ce.pos_x + dx and ce.pos_y < event.pos[1] < ce.pos_y + dx and ce.flagged == False:
                                ce.Cell_logic()
                    # if right mouse button pressed
                    elif event.button == 3:
                        for ce in Cell.cells_list:
                            if ce.pos_x < event.pos[0] < ce.pos_x + dx and ce.pos_y < event.pos[1] < ce.pos_y + dx:
                                ce.Flag()

solver = Solver()
main()