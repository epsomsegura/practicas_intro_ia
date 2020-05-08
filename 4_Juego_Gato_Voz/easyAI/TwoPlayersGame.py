from copy import deepcopy
from gtts import gTTS
import os


class TwoPlayersGame:
    # Función para ejecutar voz
    def ejecutarVoz(self,texto):
        tts = gTTS(text=texto, lang='es')
        tts.save("../src/voz.mp3")
        os.system("mpg321 ../src/voz.mp3")

    def play(self, nmoves=1000, verbose=True):
        
        history = []
        
        if verbose:
            self.show()
        
        for self.nmove in range(1, nmoves+1):
            
            if self.is_over():
                break
            
            move = self.player.ask_move(self)
            history.append((deepcopy(self), move))
            self.make_move(move)
            
            if verbose:
                texto = "Movimiento número "+str(self.nmove)+" por el jugador "+str(self.nplayer)+", el tiro se realizó en la casilla "+str(move)
                self.ejecutarVoz(texto)
                print( "\nMovimiento #%d: jugador %d tiró %s :"%(
                             self.nmove, self.nplayer, str(move)) )
                self.show()
                
            self.switch_player()
        
        history.append(deepcopy(self))
        
        return history
    
    @property
    def nopponent(self):
        return 2 if (self.nplayer == 1) else 1
    
    @property
    def player(self):
        return self.players[self.nplayer- 1]
    
    @property
    def opponent(self):
        return self.players[self.nopponent - 1]
    
    def switch_player(self):
        self.nplayer = self.nopponent

    def copy(self):
        return deepcopy(self)
