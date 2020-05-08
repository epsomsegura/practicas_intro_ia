# Librerias
import nltk
from nltk import grammar, parse
from nltk import load_parser 
from nltk.parse.generate import generate

class grammar_eval:
    # Constructor
    def __init__(self):
        self.test=""

    # Función para evaluar la semántica de una cadena
    def evalSemantics(self, text):
        sems=""
        resp=[]

        cp = load_parser('src/semantics/semantics.fcfg', trace=0)  
        tokens = text.split()

        try:
            for tree in cp.parse(tokens):
                sems = str(tree.label()['sem'])
            

            print(sems)

            verb=sems.split("(")[0]
            nouns = sems.split("(")[1].replace(")","").split(",")
            resp.append(verb)
            
            for n in nouns:
                resp.append(n)

            return resp
        except:
            return "NOSEMANTICS"