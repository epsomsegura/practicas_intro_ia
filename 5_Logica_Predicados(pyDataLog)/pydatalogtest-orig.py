from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z,works_in,manager,indirect_manager')

+ works_in('Mary', 'Production')
+ works_in('Sam',  'Marketing')
+ works_in('John', 'Production')
+ works_in('John', 'Marketing')

# give me all the X that work in Marketing
print(works_in(X,  'Marketing'))
#print

# give me all X,Y
print(works_in(X, Y))
#print

#- works_in('John', 'Production')

# give me all X,Y
#print(works_in(X, Y))
#print

#
+ manager('Mary','John')
+ manager('Sam','Mary')
+ manager('Tom','Mary')

# one of the indirect manager of X is Y, if the (direct) manager of X is Y
indirect_manager(X,Y) <= manager(X,Y)
# another indirect manager of X is Y, if there is a Z so that the manager of X is Z, 
#   and an indirect manager of Z is Y
indirect_manager(X,Y) <= manager(X,Z) & indirect_manager(Z,Y)

#
print(indirect_manager('Sam',Y))
#print(indirect_manager(X,'John'))


indirect_manager('Sam',Y)
resultado=Y.data[1]
print("resultado", resultado)


# + parent(bill, 'John Adams')
pyDatalog.assert_fact('parent', 'bill','John Adams')
print(pyDatalog.ask('parent(bill,X)'))

# specify what an ancestor is
pyDatalog.load("""
    ancestor(X,Y) <= parent(X,Y)
    ancestor(X,Y) <= parent(X,Z) & ancestor(Z,Y)
""")

# prints a set with one element : the ('bill', 'John Adams') tuple
W = pyDatalog.ask('parent(bill,X)')
print(W.answers[0][0])
#
W = pyDatalog.ask('ancestor(bill,X)')
print('Bill es ancestro de:',W.answers[0][0])

# - parent(bill, 'John Adams')
pyDatalog.retract_fact('parent', 'bill','John Adams')

W = pyDatalog.ask('parent(bill,X)')
if (W.__str__()!='None'):
    print(W.__str__())
else:
    print('No hay resultados')
