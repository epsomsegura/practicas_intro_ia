from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z,works_in,is_manager_of,is_indirect_manager_of')

# Crear hechos
+ works_in('Mary','Production')
+ works_in('Sam','Marketing')
+ works_in('John','Production')
+ works_in('John', 'Marketing')

+ is_manager_of('Mary','John')
+ is_manager_of('Sam','Mary')
+ is_manager_of('Tom','Mary')


# REGLAS
# Jefe indirecto
is_indirect_manager_of(X,Y) <= is_manager_of(X,Y)
is_indirect_manager_of(X,Y) <= is_manager_of(X,Z) & is_indirect_manager_of(Z,Y)

# print(is_indirect_manager_of(X,Y))

# AGREGAR HECHOS AL VUELO
pyDatalog.assert_fact('parent','bill', 'John Adams')
W=pyDatalog.ask('parent(Z,X)')

print(W.answers[0][1])
