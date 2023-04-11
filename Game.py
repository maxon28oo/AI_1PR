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


time_to_PC_move = 1*1000
PC_move = False

class Button:
    def __init__(self, color, x, y, width, height, text='',outline=None, function=None):
        self.color = color
        self.outline = outline
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.function = function

    def draw(self, screen, font_size=30):
        # Call this method to draw the button on the screen
        if self.outline:
            pg.draw.rect(screen, self.outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        _color = self.color
        if self.is_hovered(pg.mouse.get_pos()):
            _color = (_color[0]-20, _color[1]-20, _color[2]-20)
        pg.draw.rect(screen, _color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pg.font.Font(None, font_size)
            text = font.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_hovered(self, pos):
        # Call this method to see if a position is over the button
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        
        return False

    def is_clicked(self, event):
        # Call this method to see if the button is clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    return True
        
        return False

    def call_function(self):
        if self.function:
            self.function()


PC_move, time_to_PC_move, PC_next_move= False, 1.5*1000, None

Board = ab.Board()

#game state 0 - selecting who to play with(pc, friend), 1 - chosing who starts, 2 - playing
game_state = 0
game_opponent = 0 #0 - pc, 1 - friend, 2 - pc vs pc
who_is_first = 0 #0 - player 1, 1 - player 2(pc) 

isnt_valid = ()
valid_moves = []

widgets = []
#put 4 pieces in the middle of the board(2 black, 2 white)

#game functions
def draw_board():
    for y in range(8):
        for x in range(8):
            pg.draw.rect(screen, BLACK, (x*75, y*75, 75, 75), 1)
            if (x,y)==isnt_valid:
                pg.draw.rect(screen, (255,0,0), (x*75+1, y*75+1, 74, 74))
            elif (x,y) in valid_moves:
                pg.draw.rect(screen, (255,255,0), (x*75+1, y*75+1, 74, 74))
            else:
                pg.draw.rect(screen, GREEN, (x*75+1, y*75+1, 74, 74))

def draw_pieces():
    for y in range(8):
        for x in range(8):
            if Board.field[y][x] == "B":
                pg.draw.circle(screen, BLACK, (x*75+37, y*75+37), 30)
            elif Board.field[y][x] == "W":
                pg.draw.circle(screen, WHITE, (x*75+37, y*75+37), 30)
            elif (x,y) == PC_next_move:
                pg.draw.circle(screen, M_GRAY, (x*75+37, y*75+37), 30)


def GameSetup():
    #dispose buttons
    global game_state, PC_move, time_to_PC_move, PC_next_move
    widgets.clear()
    
    game_state = 2
    if game_opponent == 0 or game_opponent == 2:
        ab.build_tree(ab.Node(Board), ab.depth)
        if who_is_first == 1 or game_opponent == 2:
            PC_move = True
            time_to_PC_move = 1.5 * 1000
            PC_next_move = ab.best_move(ab.Node(Board))

def drawGame():
    draw_board()
    draw_pieces()
    pg.display.update()



def MenuSetup():
    global game_state
    game_state = 0
    widgets.clear()
    play_with_pc = Button(M_GRAY, 200, 200, 200, 50, 'Play with PC',outline=BLACK, function= lambda: setGameOpponent(0))
    play_with_friend = Button(M_GRAY, 200, 300, 200, 50, 'Play with friend',outline=BLACK, function= lambda: setGameOpponent(1))
    PC_with_PC = Button(M_GRAY, 200, 400, 200, 50, 'PC vs PC',outline=BLACK, function= lambda: setGameOpponent(2))
    widgets.append(play_with_pc)
    widgets.append(play_with_friend)
    widgets.append(PC_with_PC)


def setGameOpponent(_game_opponent):
    global game_opponent
    print('game opponent set to', _game_opponent)
    game_opponent = _game_opponent
    MenuPost()
    

def drawMenu():
    screen.fill(WHITE)
    #add to buttons to choose who to play with
    
    for widget in widgets:
        widget.draw(screen,30)
    pg.display.update()
    


def WinRender():
    screen.fill(WHITE)
    font = pg.font.Font(None, 100)
    
    if Board.get_winner() == "B":
        text = font.render('Black wins' + ("(You)" if who_is_first == 0  and game_opponent==0 else ("(PC)" if who_is_first == 1  and game_opponent==0 else "")), 1, BLACK)
    elif Board.get_winner() == "W":
        text = font.render("White wins" + ("(You)" if who_is_first == 0  and game_opponent==0 else ("(PC)" if who_is_first == 1  and game_opponent==0 else "")), 1, BLACK)
    else:
        text = font.render('Draw', 1, BLACK)

    screen.blit(text, (0,200))
    pg.display.update()

def setGameTurn(_game_turn):
    global who_is_first
    print('game turn set to', _game_turn)
    who_is_first = _game_turn
    Board.maximizing = True
    GameSetup()

def MenuPost():
    widgets.clear()
    if game_opponent == 1 or game_opponent == 2:
        GameSetup()
    elif game_opponent == 0:
        #add to buttons to choose who starts the game player or pc
        player_starts = Button(M_GRAY, 200, 200, 200, 50, 'Player starts',outline=BLACK, function= lambda: setGameTurn(0))
        pc_starts = Button(M_GRAY, 200, 300, 200, 50, 'PC starts',outline=BLACK, function= lambda: setGameTurn(1))
        back = Button(M_GRAY, 200, 400, 200, 50, 'Back',outline=BLACK, function= lambda: MenuSetup())
        widgets.append(player_starts)
        widgets.append(pc_starts)
        widgets.append(back)


                
def MouseClick(event):
    global valid_moves, PC_move, time_to_PC_move, PC_next_move, game_state
    
    if ( who_is_first == 1 and Board.turn == "B" and game_opponent == 0) or (who_is_first == 0 and Board.turn == "W" and game_opponent == 0) or game_opponent == 2:
        return
    Board.make_move(event.pos[0]//75, event.pos[1]//75)
    valid_moves = []

    if Board.field[event.pos[1]//75][event.pos[0]//75] == " ":
        return

    if Board.is_game_over():
        game_state = 3
        return

    if game_opponent == 0 and (Board.turn == "B" and who_is_first == 1 or Board.turn == "W" and who_is_first == 0):
        PC_move = True
        time_to_PC_move = 1.5 * 1000
        PC_next_move = ab.best_move(ab.Node(Board))


def predictMove(event):
    
    global isnt_valid, valid_moves

    x = event.pos[0]//75
    y = event.pos[1]//75
    if x<0 or x>7 or y<0 or y>7:
        return

    valid_moves = Board.legal_moves.get((x,y), [])
    if valid_moves == []:
        isnt_valid = (x,y)
    else:
        isnt_valid = ()

        #if the place is not empty, draw a red square with alpha 0.5


def main():
    run = True
    global PC_move, time_to_PC_move, game_state, PC_next_move
    while run:
        clock.tick(60)
        if game_state == 0 or game_state == 1:
            drawMenu()
        elif game_state == 2:
            drawGame()
        elif game_state == 3:
            WinRender()
        if PC_move and time_to_PC_move > 0:
            time_to_PC_move -= clock.get_time()
            if time_to_PC_move <= 0:
                Board.make_move(*PC_next_move)
                if game_opponent == 2:
                    PC_next_move = ab.best_move(ab.Node(Board))
                    time_to_PC_move = 1.5 * 1000
                else:
                    PC_move = False

                if Board.is_game_over():
                    game_state = 3


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEMOTION:
                if game_state == 2:
                    if ( who_is_first == 1 and Board.turn == "B" and game_opponent == 0) or (who_is_first == 0 and Board.turn == "W" and game_opponent == 0) or game_opponent == 2:
                        break
                    predictMove(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if game_state == 0:
                    for widget in widgets:
                        if isinstance(widget, Button):
                            if widget.is_clicked(event):
                                widget.function()
                elif game_state == 2:
                    MouseClick(event)
                elif game_state == 3:
                    MenuSetup()
                
        
                            
        
    pg.quit()

if __name__ == '__main__':
    
    MenuSetup()
    main()