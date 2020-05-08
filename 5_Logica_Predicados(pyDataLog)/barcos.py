from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z,steamboat,sailboat,rowboat,is_faster_that,input')

# HECHOS
+ steamboat('titanic')
+ sailboat('mistral')
+ rowboat('pondarrow')

#   REGLAS
is_faster_that(X,Y) <= steamboat(X) & sailboat(Y)
is_faster_that(Y,Z) <= sailboat(Y) & rowboat(Z)
is_faster_that(X,Z) <= is_faster_that(X,Y) & is_faster_that(Y,Z)

# Evaluación
barco = is_faster_that('titanic','pondarrow')

# Resultado
if str(barco) != '[()]':
    print('La afirmación es falsa')
else:
    print('La afirmación es verdadera')