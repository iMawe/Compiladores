from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree
import sys
import pandas as pd

import graphviz
from graphviz import Digraph
from graphviz import Source

import enum

class symbolTable:
    def __init__(self, id, typ, category, father = 'main', line = None):
        self.id = id
        self.type = typ
        self.category = category
        self.line = line
        self.father = father

symbol_table_array = []

gbl_nombre_function = 'main'

def insertST(node_hermano):
    symbol = symbolTable(node_hermano.lexeme, node_hermano.symbol.symbol, node_hermano.type, node_hermano.father, node_hermano.line)
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
                print("Aqui se crea uan variable", hermano.lexeme)
                #buscar si existe, true error semantico (ya definida)
                #insertar en tabla
                insertST(hermano)
    if node.symbol.symbol == 'id':
        #print("uso la variable", node.lexeme)
        #buscar en la tabla, false error semantico (variable no definida)
        if (findST):
            print("Variable encontrada")
        else:
            print("FATAL ERROR SEM VARIABLE NO DEFINIDA")

    for child in node.children:
        findVal(child)


file_name = sys.argv[1]

# lexer
tokens = get_tokens(file_name)
tokens.append([ '$', None, None ])

root, node_list = parser(tokens)

print(root.symbol.symbol)
primer_hijo = root.children[0]
print(primer_hijo.symbol.symbol)

findVal(root)

printST()