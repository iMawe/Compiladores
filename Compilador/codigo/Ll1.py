from AnalizadorLex import get_tokens
import sys
import pandas as pd

import graphviz
from graphviz import Digraph
from graphviz import Source
import math

counter = 0
dot = ''
#parser

def print_stack(stack):
    print("STACK -> ", end='')
    for element in stack:
        #print(element.symbol + ':' + str(element.is_terminal), end=' ')
        print(element.symbol, end=' ')
    print()

def print_input(input):
    print("INPUT -> ", end='')
    for element in input:        
        print(element[0], end=' ')
    print()

# retorna un nodo del arbol suntáctico segun el id
def find_in_tree(node_list, id):
    for nod in node_list:
        if nod.symbol.id == id:
            return nod
    