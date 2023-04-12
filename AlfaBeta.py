#Alpha Beta Pruning Algorithm for Reversi Game with Depth 3
import random


depth = 3


class Board:
    def __init__(self, field=None, turn=None, score=None, free_cells=None, maximizing=True, legal_moves=None):
        if field is None:
            self.field = [[' ' for i in range(8)] for j in range(8)]
            self.field[3][3] = 'W'
            self.field[3][4] = 'B'
            self.field[4][3] = 'B'
            self.field[4][4] = 'W'
        else:
            self.field = field
        if turn is None:
            self.turn = 'B'
        else:
            self.turn = turn

        if score is None:
            self.score = {
                'B': 2,
                'W': 2
            }
        else:
            self.score = score

        if free_cells is None:
            self.free_cells = 60
        else:
            self.free_cells = free_cells
        
        self.maximizing = maximizing

        if legal_moves is None:
            self.legal_moves = self.get_legal_moves()
        else:
            self.legal_moves = legal_moves

    def is_game_over(self):
        if self.free_cells == 0:
            print("game over because of no free cells")
            return True
        if self.score['B'] == 0 or self.score['W'] == 0:
            print("game over because of no pieces for one player left")
            return True
        if len(self.legal_moves) == 0:
            print("skipping " + self.turn + " turn because of no legal moves")
            self.turn = 'W' if self.turn == 'B' else 'B'
            self.maximizing = not self.maximizing
            self.legal_moves = self.get_legal_moves()
            if len(self.legal_moves) == 0:
                print("game over because of no legal moves for both players")
                return True
        return False


    def __str__(self) -> str:
        return str("\n".join([str(i) for i in self.field]))

    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Board):
            return self.field == __value.field and self.turn == __value.turn and self.score == __value.score and self.free_cells == __value.free_cells and self.legal_moves == __value.legal_moves 
        return False


    def get_winner(self):
        if self.score['B'] > self.score['W']:
            return 'B'
        if self.score['B'] < self.score['W']:
            return 'W'
        return 'D'

    def get_legal_moves(self):
        moves = {}
        for y in range(8):
            for x in range(8):
                if self.field[y][x] == ' ':
                    _moves = self.check_move(x, y)
                    if _moves is not None and len(_moves) > 0:
                        moves[(x, y)] = _moves
        return moves

    def check_move(self, x, y):
        if self.field[y][x] != ' ':
            return []
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                _move = self.check_direction(x + i, y + j, i, j, 0)
                if _move is not None:
                    moves.append(_move)
        return moves

    def check_direction(self, x, y, dx, dy, count):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return None
        if self.field[y][x] == ' ':
            return None
        if self.field[y][x] == self.turn and count > 0:
            return (x, y)
        if self.field[y][x] == self.turn and count == 0:
            return None
        return self.check_direction(x + dx, y + dy, dx, dy, count + 1)

    def make_move(self, x, y):

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        if self.field[y][x] != ' ':
            return False
        if (x, y) not in self.legal_moves:
            return False
    
        self.field[y][x] = self.turn
        self.free_cells -= 1
        self.score[self.turn] += 1
        for move in self.legal_moves[(x, y)]:
            self.flip_cells(move[0], move[1], x, y)
        

        #print(self.score)

        self.turn = 'W' if self.turn == 'B' else 'B'
        self.maximizing = not self.maximizing
        self.legal_moves = self.get_legal_moves()
        return True
    
    def flip_cells(self, x1, y1, x2, y2):
        dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
        x = x1
        y = y1
        while x != x2 or y != y2:
            if (x, y) != (x1, y1):
                self.field[y][x] = self.turn
                self.score[self.turn] += 1
                self.score['W' if self.turn == 'B' else 'B'] -= 1
            x += dx
            y += dy

class Node:
    def __init__(self, board, move=None):
        self.board = board
        self.move = move
        self.score = None
        self.is_leaf = False

    def game_over(self):
        return self.board.is_game_over()

    def get_score(self):
        return self.score

    def __repr__(self):
        return str(self.board) + " " + str(self.move) + " " + str(self.score) + " " + str(self.is_leaf)
    
    def __hash__(self) -> int:
        return hash(str(self.board))
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Node):
            return self.board == __value.board
        return False


class Tree:
    def __init__(self):
        self.root = None
        self.tree = {}

    def get_root(self):
        return self.root

    def add_root(self, obj):
        self.root = obj
    def add_node(self, obj, parent):
        if parent not in self.tree:
            self.tree[parent] = []
        self.tree[parent].append(obj)

    def get_children(self, obj):
        return self.tree.get(obj, [])
    
    def clear(self):
        self.tree.clear()
tree = Tree()
    

def build_tree(node, depth):
    if depth == 0 or node.game_over():
        node.score = abs(node.board.score['B'] - node.board.score['W'])
        node.is_leaf = True
        return
    for move in node.board.legal_moves:
        board = Board([row[:] for row in node.board.field], node.board.turn,node.board.score.copy(), node.board.free_cells, node.board.maximizing,{move: node.board.legal_moves[move]})
        board.make_move(move[0], move[1])
        
        #print(board,end='\n\n')
        child = Node(board, move)
        tree.add_node(child, node)
        build_tree(child, depth - 1)



def alphabeta(node, depth, alpha, beta):
    if node.is_leaf:
        return node.score
    if node.board.maximizing:
        v = -100000000
        for child in tree.get_children(node):
            v = max(v, alphabeta(child, depth - 1, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        
    else:
        v = 100000000
        for child in tree.get_children(node):
            v = min(v, alphabeta(child, depth - 1, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break

    node.score = v
    return v
    

def best_move(node):
    if tree.get_children(node) == []:
        tree.clear()
        tree.add_root(node)
        build_tree(node, depth)



    scores_moves = [(alphabeta(child, depth - 1, -100000000, 100000000), child.move) for child in tree.get_children(node)]
    if node.board.maximizing:
        best_score, best_move = max(scores_moves, key=lambda x: x[0])
    else:
        best_score, best_move = min(scores_moves, key=lambda x: x[0])
    #if there are multiple moves with the same score, choose one at random
    best_moves = [move for score, move in scores_moves if score == best_score]
    if len(best_moves) > 1:
        best_move = random.choice(best_moves)

    print("Best move is: " + str(best_move) + " with score " + str(best_score))
    return best_move

    