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
        print(element.symbol, end=' ')
    print()

def print_input(input):
    print("INPUT -> ", end='')
    for element in input:        
        print(element[0], end=' ')
    print()

def find_in_tree(node_list, id):
    for nod in node_list:
        if nod.symbol.id == id:
            return nod

def print_tree(node, node_list, info = False):
    global dot
    dot = "digraph G { \n"

    for nod in node_list:
        if nod.symbol.is_terminal:
            if nod.symbol.symbol == 'e':
                dot += str(nod.symbol.id) + ' [ style=filled fillcolor=yellow  label=< <b>' + nod.symbol.symbol + '</b> > ]; \n'
            else:
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme
                dot += str(nod.symbol.id) + ' [ style=filled fillcolor=yellow  label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(lexeme) + ' <br/> line ' + str(nod.line)  + '<br/>' + str(nod.type)+' > ]; \n' #+ '<br/>' + str(nod.type)
        
        else:#ANALIZADOR SEMANTICO

            if info and (nod.symbol.symbol == 'E' or nod.symbol.symbol == 'T' or nod.symbol.symbol == "E'" or nod.symbol.symbol == 'TERM' or nod.sumbol.symbol == 'IF_DECL' or nod.symbol.symbol == 'WHILE_DECL' or nod.symbol.symbol == 'FOR_DECL'):
                lexeme = nod.lexeme
                lexeme = "&#38;" if lexeme == '&' else nod.lexeme

                if nod.visited == True:
                    dot += str(nod.symbol.id) + ' [ style=filled fillcolor=green label=< <b>' + nod.sumbol.symbol + '</b> <br/> ' + str(nod.type) + ' <br/> line ' + str(nod.line) + ' > ]; \n'
                else:
                    dot += str(nod.symbol.id) + ' [ label=< <b>' + nod.symbol.symbol + '</b> <br/>' + str(nod.type) + ' > ]; \n'
            
            else:
                dot += str(nod.symbol.id) + ' [ label=" ' + nod.symbol.symbol + ' " ]; \n'
    
    print_tree_recursive(node)
    dot += "}"

    #print(dot)

    graph = graphviz.Source(dot, format= 'png')
    graph.render("tree.png", view=True)

def print_tree_recursive(node):
    global dot
    tmp = []
    for child in node.children:
        dot += str(node.symbol.id) + ' -> ' + str(child.symbol.id) + '; \n'
        tmp.append(str(child.symbol.id))
        print_tree_recursive(child)
    
    if len(node.children) > 0:
        dot += "{ \n"
        dot += "    rank = same; \n"
        dot += "    edge[ style=invis]; \n"
        dot += " -> ".join(tmp) + "; \n"
        dot += "    rankdir = LR; \n"
        dot += "} \n"

def update_stack(root, node_list, syntax_table, stack, current_token):
    production = syntax_table.loc[ stack[0].symbol, current_token]


    if str(production) == "nan":
        return False
    
    productions = production.split(" ")
    productions.pop(0)
    productions.pop(0)

    father = stack.pop(0)
    node_father = find_in_tree(node_list, father.id)

    if productions[0] == "''":
        new_symbol = node_stack('e', True)
        nod_tree = node_parser(new_symbol, None, [], node_father)
        node_father.children.insert(0, nod_tree)
        node_list.append(nod_tree)
        return True
    for prod in reversed(productions):
        new_symbol = node_stack(prod, False if prod.isupper() else True)
        stack.insert(0, new_symbol)

        nod_tree = node_parser(new_symbol, None, [], node_father)
        node_father.children.insert(0, nod_tree)
        node_list.append(nod_tree)

    return True

class node_stack:
    def __init__(self, symbol, terminal):
        global counter
        self.id = counter
        self.symbol = symbol
        self.is_terminal = terminal
        counter += 1

class node_parser:
    def __init__(self, symbol, lexeme = None, childern = [], father = None, line = None):
        self.symbol = symbol
        self.lexeme = lexeme
        self.line = line
        self.children = childern
        self.father = father
        self.type = None

syntax_table = pd.read_csv("sytax_table.csv", index_col=0)

symbol1 = node_stack( '$', True)
symbol2 = node_stack('PROGRAM', False)
stack = []
stack.insert(0, symbol1)
stack.insert(0, symbol2)

root = node_parser(symbol2)
node_list = []
node_list.append(root)

def parser(tokens):
    result = False
    while True:
        if stack[0].symbol == tokens[0][0] == '$':
            result = True
            break
        if stack[0].is_terminal:
            if stack[0].symbol == tokens[0][0]:
                nod = find_in_tree(node_list, stack[0].id)
                nod.lexeme = tokens[0][1]
                nod.line = tokens[0][2]

                stack.pop(0)
                tokens.pop(0)
            else:
                result = False
                print("Syntax FATAL ERROR 1 at line ", tokens[0][2])
                break
        else:
            if not update_stack(root, node_list, syntax_table, stack, tokens[0][0]):
                result = False
                print("Syntax FATAL ERROR 2 at line ", tokens[0][2])
                break
    if(result == False):
        print("no pertenece al lenguaje")
    elif(result == True):
        #print_tree(root, node_list)
        print("si pertenece al lenguaje")

    return root, node_list

if __name__ == "__main__":

    # source code
    file_name = sys.argv[1]

    # lexer
    tokens = get_tokens(file_name)
    tokens.append([ '$', None, None ])


    parser(tokens)
