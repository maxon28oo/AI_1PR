#Reversi game
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg


import AlfaBeta as ab

#pygame simple setup
pg.init()
pg.display.set_caption('Reversi')
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
M_GRAY = (121, 131, 131)




B = ab.Board()
n = ab.Node(B)
ab.tree.add_root(n)
ab.build_tree(n, ab.depth, True)



def draw_board():
    for y in range(8):
        for x in range(8):
            pg.draw.rect(screen, BLACK, (x*75, y*75, 75, 75), 1)
            pg.draw.rect(screen, GREEN, (x*75+1, y*75+1, 74, 74))

def draw_pieces(board):
    for y in range(8):
        for x in range(8):
            if board.field[y][x] == "B":
                pg.draw.circle(screen, BLACK, (x*75+37, y*75+37), 30)
            elif board.field[y][x] == "W":
                pg.draw.circle(screen, WHITE, (x*75+37, y*75+37), 30)




def main(node):
    print(node.board)
    print(len(ab.tree.get_children(node)))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in ab.tree.get_children(node):
                    main(i)
                return
        screen.fill(M_GRAY)
        draw_board()
        draw_pieces(node.board)
        pg.display.update()
        clock.tick(60)
    

main(n)