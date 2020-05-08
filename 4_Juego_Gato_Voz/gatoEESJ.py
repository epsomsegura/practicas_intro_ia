# Librerias
import speech_recognition as sr
from gtts import gTTS
import os
import nltk
from nltk import grammar, parse
from nltk import load_parser 
from nltk.parse.generate import generate
from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player

# Clase agregada para la interacción mediante la voz
class Voz_Control(object):
    # Constructor
    def __init__(self):
        self.test=""
    
    # Ejecutar voz
    def ejecutarVoz(self,texto):
        tts = gTTS(text=texto, lang='es')
        tts.save("src/voz.mp3")
        os.system("mpg321 src/voz.mp3")

    # Reconocer voz
    def reconocerVoz(self):
        flag=True
        texto = ""
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        while(flag):
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                texto = r.recognize_google(audio, language="es-MX")
                flag = False
            except sr.UnknownValueError:
                self.ejecutarVoz('No pude reconocer lo que dijiste, intenta de nuevo')
                self.reconocerVoz()
            except sr.RequestError as e:
                self.ejecutarVoz('No pude procesar tu voz, intenta de nuevo')
                self.reconocerVoz()

        return texto
    
    # Bienvenida al juego
    def bienvenida(self):
        texto = "Hola, que tal, ¿te gustaría jugar una partida de gato?"
        self.ejecutarVoz(texto)
        resp = self.reconocerVoz()
        print(resp)
        if (resp == "si" or resp == "claro" or resp == "sí"):
            self.ejecutarVoz("Perfecto, comencemos")
            self.instrucciones()
            return True
        else:
            self.ejecutarVoz("Okay, será en otro momento")
            return False

    # Instrucciones
    def instrucciones(self):
        texto = "El juego se basa en las posiciones disponibles, iniciando de derecha a izquierda, de arriba hacia abajo, "
        texto += "cada casilla corresponde a un número del 1 al 9, el número de casillas disponibles se reduce por cada jugada de cada jugador. "
        texto += "...Para tirar en tu turno debes decir...tirar en la casilla, seguido del número que eligió para tirar."
        self.ejecutarVoz(texto)

    # gramática
    def gramatica(self,texto):
        print(texto)
        flag = True
        x = ""
        gramatica2 = grammar.FeatureGrammar.fromstring("""
                % start S
                S[SEM=<?vp(?np)>] -> VP[SEM=?vp] NP[SEM=?np]
                S[SEM=<jugar(?np)>] -> NP[SEM=?np]
                
                VP[SEM=?v] -> V[SEM=?v] PREPO
                V[SEM=<\\x.jugar(x)>] -> "tirar" | "jugar" | "poner" 
                PREPO -> "en"
                
                NP[SEM=?num] -> ARTICULO SUSTANTIVO NUM[SEM=?num]
                NP[SEM=?num] -> PREPO ARTICULO NUM[SEM=?num]
                NP[SEM=?num] -> ARTICULO NUM[SEM=?num]
                ARTICULO -> "el" | "la"
                SUSTANTIVO -> "casilla" | "posición" | "número" | "espacio"
                
                NUM[SEM=<1>] -> "1" | "uno"
                NUM[SEM=<2>] -> "2" | "dos"
                NUM[SEM=<3>] -> "3" | "tres"
                NUM[SEM=<4>] -> "4" | "cuatro"
                NUM[SEM=<5>] -> "5" | "cinco"
                NUM[SEM=<6>] -> "6" | "seis"
                NUM[SEM=<7>] -> "7" | "siete"
                NUM[SEM=<8>] -> "8" | "ocho"
                NUM[SEM=<9>] -> "9" | "nueve"
            """)

        while (flag):
            try:
                parser = parse.FeatureEarleyChartParser(gramatica2)
                tokens = texto.split()
                tree = parser.parse_one(tokens)
                semantica = tree.label()['SEM']
                x = (str(semantica).split("("))[1].replace(")","")
                flag=False
            except:
                self.ejecutarVoz("No pude reconocer lo que dijiste, intenta de nuevo")
                texto = self.reconocerVoz()
                self.gramatica(texto)
        
        return x
        


# Clase jugador humano
class MyHuman_Player(Human_Player):
    # Instanciar clase
    VC = Voz_Control()

    # Preguntar por movimiento
    def ask_move(self, game):
        possible_moves = game.possible_moves()
        possible_moves_str = list(map(str, game.possible_moves()))
        texto = "Jugador "+str(game.nplayer)+", ¿En que casilla disponible desea tirar?"
        VC.ejecutarVoz(texto)
        move = "NO_MOVE_DECIDED_YET"
        move = VC.reconocerVoz()
        pos = VC.gramatica(move)
        move = "move #"+str(pos)
        while True:
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
                VC.ejecutarVoz("El tiro se aplicó en la posición X")
                move = possible_moves[possible_moves_str.index(str(move))]
                return move
            
# Clase controlador del juegp
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


# Inicio del algoritmo
if __name__ == "__main__":
    # Define the algorithm
    algorithm = Negamax(7)

    # Start the game
    VC = Voz_Control()
    if(VC.bienvenida()):
        GameController([MyHuman_Player(), AI_Player(algorithm)]).play()

