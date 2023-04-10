#Reversi game
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg


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




class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.rect = pg.Rect(x*75, y*75, 75, 75)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x*75+37, self.y*75+37), 30)

    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            return True
        
        return False

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    return True
        
        return False

    def call_function(self):
        if self.function:
            self.function()



#game state 0 - selecting who to play with(pc, friend), 1 - chosing who starts, 2 - playing
game_state = 0
game_opponent = 0 #0 - pc, 1 - friend
game_turn = 0 #0 - black, 1 - white
who_is_first = 0 #0 - player 1, 1 - player 2(pc)

isnt_valid = ()
valid_moves = []

score = {
    BLACK: 2,
    WHITE: 2
}



#game variables
Stage = [['' for _ in range(8)] for _ in range(8)]
widgets = []
#put 4 pieces in the middle of the board(2 black, 2 white)
Stage[4][4] = Piece(WHITE, 4, 4)
Stage[3][3] = Piece(WHITE, 3, 3)
Stage[3][4] = Piece(BLACK, 4, 3)
Stage[4][3] = Piece(BLACK, 3, 4)


#game functions
def draw_board():
    for y in range(8):
        for x in range(8):
            pg.draw.rect(screen, BLACK, (x*75, y*75, 75, 75), 1)
            if (x,y)==isnt_valid:
                pg.draw.rect(screen, (255,0,0), (x*75+1, y*75+1, 74, 74))
            elif (x,y) in [i[:-2] for i in valid_moves]:
                pg.draw.rect(screen, (255,255,0), (x*75+1, y*75+1, 74, 74))
            else:
                pg.draw.rect(screen, GREEN, (x*75+1, y*75+1, 74, 74))

def draw_pieces():
    for y in range(8):
        for x in range(8):
            if Stage[y][x] != '':
                Stage[y][x].draw(screen)


def GameSetup():
    #dispose buttons
    global game_state
    widgets.clear()
    
    game_state = 2

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
    widgets.append(play_with_pc)
    widgets.append(play_with_friend)


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
    if score[BLACK] > score[WHITE]:
        text = font.render('Black wins', 1, BLACK)
    elif score[BLACK] < score[WHITE]:
        text = font.render('White wins', 1, WHITE)
    else:
        text = font.render('Draw', 1, BLACK)
    screen.blit(text, (200, 200))
    pg.display.update()

def setGameTurn(_game_turn):
    global who_is_first
    print('game turn set to', _game_turn)
    who_is_first = _game_turn
    GameSetup()

def MenuPost():
    widgets.clear()
    if game_opponent == 1:
        GameSetup()
    elif game_opponent == 0:
        #add to buttons to choose who starts the game player or pc
        player_starts = Button(M_GRAY, 200, 200, 200, 50, 'Player starts',outline=BLACK, function= lambda: setGameTurn(0))
        pc_starts = Button(M_GRAY, 200, 300, 200, 50, 'PC starts',outline=BLACK, function= lambda: setGameTurn(1))
        back = Button(M_GRAY, 200, 400, 200, 50, 'Back',outline=BLACK, function= lambda: MenuSetup())
        widgets.append(player_starts)
        widgets.append(pc_starts)
        widgets.append(back)




def makeMove(event):
    global game_turn
    color = BLACK if game_turn == 0 else WHITE
    #get mouse position in the board
    x = event.pos[0]//75
    y = event.pos[1]//75
    if x<0 or x>7 or y<0 or y>7:
        return
    #check if the place is empty
    valid_moves = getValidMoves(x,y, BLACK if game_turn == 0 else WHITE)
    if valid_moves != []:
        Stage[y][x] = Piece(color, x, y)
        score [color] += 1
        #change the color of the pieces
        for i in valid_moves:
            pos = [x,y]
            while tuple(pos) != i[:-2]:
                Stage[pos[1]][pos[0]].color = color
                score [color] += 1
                pos[0] += i[2]
                pos[1] += i[3]

        game_turn = (game_turn+1)%2
        if getValidMovesForColor(BLACK if game_turn == 0 else WHITE) == []:
            print('no valid moves for', 'black' if game_turn == 0 else 'white')
            game_turn = (game_turn+1)%2
            if getValidMovesForColor(BLACK if game_turn == 0 else WHITE) == []:
                global game_state
                print('also no valid moves for', 'black' if game_turn == 0 else 'white')
                print('game over')
                game_state = 3
                



def getValidMovesForColor(color):
    valid_moves = []
    for y in range(8):
        for x in range(8):
            if Stage[y][x] == '':
                if getValidMoves(x,y,color) != []:
                    valid_moves.append((x,y))
    return valid_moves

def getValidMoves(x,y,colorOfPiece):
    #check if the move is valid and return a list of valid moves
    #check all directions to see if the move is valid

    good_moves = []
    if Stage[y][x] != '':
        return []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i==0 and j==0:
                continue
            t = checkDirection(x,y,i,j,0, colorOfPiece)
            if t != (-1,-1):
                good_moves.append(t)
    return good_moves
    

def checkDirection(x,y,dx,dy,depth, colorOfPiece):
    x += dx
    y += dy
    depth += 1

    if x<0 or x>7 or y<0 or y>7:
        return (-1,-1)
    if Stage[y][x] == '':
        return (-1,-1)
    if Stage[y][x].color != colorOfPiece:
        return checkDirection(x,y,dx,dy,depth, colorOfPiece)
    if Stage[y][x].color == colorOfPiece and depth>1:
        return (x,y,dx,dy)
    return (-1,-1)





def predictMove(event):
    
    global isnt_valid, valid_moves

    x = event.pos[0]//75
    y = event.pos[1]//75
    if x<0 or x>7 or y<0 or y>7:
        return

    valid_moves = getValidMoves(x,y, BLACK if game_turn == 0 else WHITE)
    if valid_moves == []:
        isnt_valid = (x,y)
    else:
        isnt_valid = ()

        #if the place is not empty, draw a red square with alpha 0.5


def main():
    run = True
    while run:
        clock.tick(60)
        if game_state == 0 or game_state == 1:
            drawMenu()
        elif game_state == 2:
            drawGame()
        elif game_state == 3:
            WinRender()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEMOTION:
                if game_state == 2:
                    predictMove(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if game_state == 0:
                    for widget in widgets:
                        if isinstance(widget, Button):
                            if widget.is_clicked(event):
                                widget.function()
                elif game_state == 2:
                    makeMove(event)
                elif game_state == 3:
                    MenuSetup()
                
        
                            
        
    pg.quit()

if __name__ == '__main__':
    
    MenuSetup()
    main()