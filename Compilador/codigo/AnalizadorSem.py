from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree
import sys
import pandas as pd



class symbolTable:
    def __init__(self, id, typ, category, father = 'main', line = None):
        self.id = id
        self.type = typ
        self.category = category
        self.line = line
        self.father = father

symbol_table_array = []

gbl_nombre_function = 'main'

def insertST(node_var):
    symbol = symbolTable(node_var.lexeme, node_var.symbol.symbol, node_var.type, node_var.father, node_var.line)
    symbol_table_array.append(symbol)

def removeST():
    global symbol_table
    symbol_table_temp = []
    for symbol in symbol_table_array:
        if symbol.father != gbl_nombre_function:
            symbol_table_temp.append(symbol)
    symbol_table = symbol_table_temp

def findST():
    for symbol in reversed(symbol_table_array):
        if symbol.id == id:
            return True
        else: 
            return False

def printST():
    for i in symbol_table_array:
        print(i.id)

def findVal(node):
    if node.symbol.symbol == 'FUNCTION':
        tercer_hijo = node.children[2]
        gbl_nombre_function = tercer_hijo.lexeme
        print(gbl_nombre_function)

    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]

            if primer_hijo.symbol.symbol == 'TYPE':
                hermano = primer_hijo.father.children[1]
                variable = hermano.children[0]
                print("Aqui se crea una variable", variable.lexeme)
                #buscar si existe, true error semantico (ya definida)
                #insertar en tabla
                insertST(variable)
    if node.symbol.symbol == 'id':
        #print("uso la variable", node.lexeme)
        #buscar en la tabla, false error semantico (variable no definida)
        if (findST):
            print("Variable encontrada")
        else:
            print("FATAL ERROR SEM VARIABLE NO DEFINIDA")

    for child in node.children:
        findVal(child)


class tipos:
    def init(self, t, lex, tp, pos, lin,atributo, scope):
        self.token = t
        self.lexema = lex
        self.tipo = tp
        self.posicion = pos
        self.linea = lin
        self.scope = scope
        self.atributo = atributo

tabla_de_atributos = []
funcion_actual = None
funcion_actual_aux = None

def insertar_tipo(arbol):
    if arbol.elemento == "FUNC":
        tabla_de_atributos.append(
            tipos(arbol.hijos[1].token, arbol.hijos[1].token.value, "variable", arbol.hijos[1].token.lexpos,
                    arbol.hijos[1].token.lineno,arbol.hijos[0].hijos[0].token.value ,funcion_actual))
    elif arbol.elemento=="STATEMENT" and arbol.hijos[0].elemento!="EMPTY":
        tabla_de_atributos.append(
            tipos(arbol.hijos[2].token, arbol.hijos[2].token.value, "variable", arbol.hijos[2].token.lexpos,
                    arbol.hijos[2].token.lineno,arbol.hijos[1].hijos[0].token.value ,funcion_actual)) 
    for x in arbol.hijos:
        insertar_tipo(x)   

def comprobar_asignacion():
    for x in reversed(tabla_de_atributos):
        if x.tipo == "asignacion/retorno":
            for y in reversed(tabla_de_atributos):
                if y.tipo=="variable" and y.lexema==x.lexema:
                    print("correcto")
                else:
                    print("error")

for i in range(len(tabla_de_atributos)):    
   print(tabla_de_atributos[i].token,tabla_de_atributos[i].atributo)

comprobar_asignacion()
marca=False
def chek_val():
   for i in range(len(tabla_de_atributos)):
       if tabla_de_atributos[i].atributo=="asignacion":
           var=tabla_de_atributos[i-1].lexema
           for j in range(len(tabla_de_atributos)):
               if var==tabla_de_atributos[j].lexema and tabla_de_atributos[j].atributo!="asignacion retorno":
                   if tabla_de_atributos[i].token=="num " and tabla_de_atributos[j].atributo=="hun":
                       print("accion correcta")
                       marca=True
                   if tabla_de_atributos[i].token=="boolean" and tabla_de_atributos[j].atributo=="chillu":
                       print("accion correcta")
                       marca=True
                   else:
                       print("error el dato asignado no es del tipo")

contenedor_asig=[]
contenedor_mostar=[]
if(marca!=True):
    chek_val()

def almacenar(x):
  temp = type(x)is int
  return temp
file_name = sys.argv[1]





# lexer
tokens = get_tokens(file_name)
tokens.append([ '$', None, None ])

root, node_list = parser(tokens)

#print(root.symbol.symbol)
#primer_hijo = root.children[0]
#print(primer_hijo.symbol.symbol)

findVal(root)

printST()