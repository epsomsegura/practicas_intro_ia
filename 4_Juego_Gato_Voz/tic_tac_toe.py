# This is a variant of the Tic Tac Toe recipe given in the easyAI library

from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class MyHuman_Player(Human_Player):
    
    def ask_move(self, game):
        possible_moves = game.possible_moves()
        # The str version of every move for comparison with the user input:
        possible_moves_str = list(map(str, game.possible_moves()))
        move = "NO_MOVE_DECIDED_YET"
        while True:
            move = input("\nPlayer %s what do you play ? "%(game.nplayer))
            if move == 'show moves':
                print ("Possible moves:\n"+ "\n".join(
                       ["#%d: %s"%(i+1,m) for i,m in enumerate(possible_moves)])
                       +"\nType a move or type 'move #move_number' to play.")

            elif move == 'quit':
                raise KeyboardInterrupt

            elif move.startswith("move #"):
                # Fetch the corresponding move and return.
                move = possible_moves[int(move[6:])-1]
                return move

            elif str(move) in possible_moves_str:
                # Transform the move into its real type (integer, etc. and return).
                move = possible_moves[possible_moves_str.index(str(move))]
                return move
            
    
class GameController(TwoPlayersGame):
    def __init__(self, players):
        # Define the players
        self.players = players

        # Define who starts the game
        self.nplayer = 1 

        # Define the board
        self.board = [0] * 9
    
    # Define possible moves
    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]
    
    # Make a move
    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    # Does the opponent have three in a line?
    def loss_condition(self):
        possible_combinations = [[1,2,3], [4,5,6], [7,8,9],
            [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]

        return any([all([(self.board[i-1] == self.nopponent)
                for i in combination]) for combination in possible_combinations]) 
        
    # Check if the game is over
    def is_over(self):
        return (self.possible_moves() == []) or self.loss_condition()
        
    # Show current position
    def show(self):
        print('\n'+'\n'.join([' '.join([['.', 'O', 'X'][self.board[3*j + i]]
                for i in range(3)]) for j in range(3)]))
                 
    # Compute the score
    def scoring(self):
        return -100 if self.loss_condition() else 0

if __name__ == "__main__":
    # Define the algorithm
    algorithm = Negamax(7)

    # Start the game
    GameController([MyHuman_Player(), AI_Player(algorithm)]).play()

