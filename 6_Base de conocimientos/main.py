from pyDatalog import pyDatalog
# FN: Agregar en la base de conocimientos
def agregar(nombre):
    pyDatalog.assert_fact('is_sport_person',nombre)
    pyDatalog.assert_fact('is_person',nombre)
    pyDatalog.assert_fact('is_exited',nombre,'3','600')
    pyDatalog.assert_fact('has_interest_in_sports',nombre,'4','800')

    print(nombre+" se agregó a la base de conocimientos")

# FN: Buscar en la base de conocimientos
def buscar():
    print('Opciones para buscar personas\n1: Buscar a todos\n2: Buscar por nombre\n3: Volver\n')
    sel = None
    
    while sel not in ("1","2","3"):
        sel= input('Seleccione una opción:\n')
        if(sel == '1'):
            print(pyDatalog.ask("is_person(X)"))
        elif(sel == '2'):
            nombre = input("Escribe un nombre para consultar:\n")
            W = pyDatalog.ask("is_person('"+nombre+"')")

            if(str(W) == 'None'):
                op = None
                while op not in ("s","n","S","N"):
                    op = input("No existe esta persona, ¿Desea agregarla?(S/N)")
                    if(op=='s' or op=='S'):
                        agregar(nombre)
                    elif(op=="n" or op=="N"):
                        break
                    else:
                        print('Solo puede agregar S o N')
            else: 
                print(W.answers)

        elif(sel == '3'):
            break
        else:
            print("Ingrese una opción valida")


def eliminar(nombre):
    W = pyDatalog.ask("is_person('"+nombre+"')")

    if(str(W) == 'None'):
        print("Este nombre no lo conozco")
    else:
        pyDatalog.retract_fact('is_sport_person',nombre)
        pyDatalog.retract_fact('is_person',nombre)
        pyDatalog.retract_fact('is_exited',nombre,'3','600')
        pyDatalog.retract_fact('has_interest_in_sports',nombre,'4','800')

# CREACIÓN DE LAS REGLAS
pyDatalog.load("""
    is_person(X) <= is_sport_person(X)
    like_suspense(X,0,100) <= is_person(X)
    is_exited(X,3,600) <= is_sport_person(X)
    has_interest_in_sports(X,4,800) <= is_sport_person(X)
""")

# CREACION DIMAMICA DE JUANITO
pyDatalog.assert_fact('is_sport_person','Juanito')
pyDatalog.assert_fact('is_person','Juanito')
pyDatalog.assert_fact('is_exited','Juanito','3','600')
pyDatalog.assert_fact('has_interest_in_sports','Juanito','4','800')
# CREACION DIMAMICA DE PABLITO
pyDatalog.assert_fact('is_sport_person','Pablito')
pyDatalog.assert_fact('is_person','Pablito')
pyDatalog.assert_fact('is_exited','Pablito','3','600')
pyDatalog.assert_fact('has_interest_in_sports','Pablito','4','800')


print("Práctica pyDatalog dinámico\n")

print("Base de conocimiento de personas")

while True:
    print("\n\nSeleccione una opción:\n")
    print("1: Buscar persona")
    print("2: Agregar persona")
    print("3: Quitar persona")
    print("4: Finalizar\n")
    op=input("Seleccione una opción:\n")
    
    if(op=='1'):
        buscar()
    elif(op=='2'):
        agregar(input("Escribe el nombre a agregar por favor:\n"))
    elif(op=='3'):
        eliminar(input("Escribe el nombre a agregar por favor:\n"))
    elif(op=='4'):
        print("Adios")
        break