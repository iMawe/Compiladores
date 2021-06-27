from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree, update_stack
import sys
import pandas as pd



class symbolTable:
    def __init__(self, id, typ, category, father = 'uma', line = None):
        self.id = id
        self.type = typ
        self.category = category
        self.line = line
        self.father = father

symbol_table_array = []

gbl_nombre_function = 'uma'

def insertST(node_var, category, father):
    symbol = symbolTable(node_var.lexeme, node_var.type, category, father, node_var.line)
    symbol_table_array.append(symbol)

def removeST():
    global symbol_table_array
    symbol_table_temp = []
    for symbol in symbol_table_array:
        if symbol.father != gbl_nombre_function:
            symbol_table_temp.append(symbol)
    symbol_table_array = symbol_table_temp

def findST(lexeme):
    val = False
    for symbol in reversed(symbol_table_array):
        #print("PRINT SYMBOLID: ",symbol.id)
        #print("PRINT LEXEME: ", lexeme)
        if symbol.id.strip() == lexeme:
            val = True
    return val

def findSTT(lexeme):
    for symbol in reversed(symbol_table_array):
        #print("PRINT SYMBOLID: ",symbol.id)
        #print("PRINT LEXEME: ", lexeme)
        if symbol.id.strip() == lexeme:
            #print("IF SYMBOL", symbol.id)
            return symbol.type

def printST():
    for i in symbol_table_array:
        print(i.id, i.type, i.category, i.father, i.line)

def findVal(node):
    global gbl_nombre_function
    if node.symbol.symbol == 'FUNCTION':
        tercer_hijo = node.children[2]
        gbl_nombre_function = tercer_hijo.lexeme
        #print(gbl_nombre_function)

        variable_fun = node.children[2]
        insertST(variable_fun, "Funcion", gbl_nombre_function)

    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]

            if primer_hijo.symbol.symbol == 'TYPE':
                hermano = primer_hijo.father.children[1]
                variable = hermano.children[0]
                #print("Aqui se crea una variable", variable.lexeme)
                if (findST(variable.lexeme)):
                    print("ERROR SEMANTICO VARIABLE YA DEFINIDA")
                else:
                #buscar si existe, true error semantico (ya definida)
                #insertar en tabla
                    insertST(variable, "Variable", gbl_nombre_function)
    
    if node.symbol.symbol == 'id':
        #printST()
        #print(node.lexeme)
        #print("uso la variable", node.lexeme)
        #buscar en la tabla, false error semantico (variable no definida)
        if (findST(node.lexeme)):
            print("Variable encontrada")
        else:
            print("FATAL ERROR SEM VARIABLE NO DEFINIDA", node.lexeme, node.line)

    updateType(node)

    if node.symbol.symbol == 'keyr':
        #print("PADRE DE KEYR: ", node.father.symbol.symbol)
        #print("ENTRANDO A KEYR")
        if node.father.father.symbol.symbol == 'FUNCTION_M':
            #print("ENTRANDO A FUNCSTION_M")
            gbl_nombre_function = 'uma'
            removeST()
        if node.father.symbol.symbol == 'BLOCK':
            removeST()
            #print("ENTRANDO A BLOCK")

    for child in node.children:
        findVal(child)

def setType(node):
    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]

            if primer_hijo.symbol.symbol == 'TYPE':
                node_tp = primer_hijo.children[0]
                primer_hijo.father.children[1].children[0].type = node_tp.lexeme
            
    if node.symbol.symbol == 'FUNCTION':
        if len(node.children) > 0:
            node_type = node.children[0].children[0]
            node.children[2].type = node_type.lexeme

    for child in node.children:
        setType(child)

def updateType(node):
    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]
            if primer_hijo.symbol.symbol == 'id':
                #print("IF ID")
                lex = findSTT(primer_hijo.lexeme)
                #print("LEX ", lex)
                if lex:
                    primer_hijo.type = lex
                    #print("TIPO NODO LEX", primer_hijo.type)

        if len(node.children) > 2:
            #print("ENTRANDO A CHILDREN > 2")
            tercer_hijo = node.children[2]
            if tercer_hijo.symbol.symbol == 'E':
                setTypeE(tercer_hijo)

    for child in node.children:
        updateType(child)


def setTypeE(node):
    node_E = node
    node.type = 'hun'
    #print("NODE_E ", node_E.symbol.symbol)
    if node_E.children[0].symbol.symbol == 'T':
        node_TERM = node_E.children[0].children[0]
        #print("ENTRANDO NODE_T ", node_TERM.symbol.symbol)
        if node_TERM.symbol.symbol == 'TERM':
            if node_TERM.children[0].symbol.symbol == 'num':
                node_TERM.children[0].type = 'hun'
            elif node_TERM.children[0].symbol.symbol == 'id':
                lex = findSTT(node_TERM.children[0].lexeme)
                #print("IMPRIMIENDO LEX ", lex)
                if lex:
                    node_TERM.children[0].type = lex
            elif node_TERM.children[0].symbol.symbol == 'boolean':
                node_TERM.children[0].type = 'chillu'

    if node_E.children[1].symbol.symbol == 'E\'':
        setTypeEe(node_E.children[1])
        
    for child in node.children:
        setType(child)


def setTypeEe(node):
    node_Ee = node
    if len(node_Ee.children) > 1:
        #print("NODE_Ee ", node_Ee.symbol.symbol)
        node_TERM = node_Ee.children[1].children[0]
        #print("NODE_TERM ", node_TERM.symbol.symbol)
        #print("ENTRANDO NODE_T ", node_TERM.symbol.symbol)
        if node_TERM.symbol.symbol == 'TERM':
            if node_TERM.children[0].symbol.symbol == 'num':
                node_TERM.children[0].type = 'hun'

            elif node_TERM.children[0].symbol.symbol == 'id':
                #print("IMPRIMIENDO LEX NODE TERM ", node_TERM.children[0].lexeme)
                lex = findSTT(node_TERM.children[0].lexeme)
                #print("IMPRIMIENDO LEX ", lex)
                if lex:
                    node_TERM.children[0].type = lex
            elif node_TERM.children[0].symbol.symbol == 'boolean':
                node_TERM.children[0].type = 'chillu'
                    
    for child in node.children:
        setTypeEe(child)

file_name = sys.argv[1]

# lexer
tokens = get_tokens(file_name)
tokens.append([ '$', None, None ])

root, node_list = parser(tokens)

#print(root.symbol.symbol)
#primer_hijo = root.children[0]
#print(primer_hijo.symbol.symbol)
setType(root)
findVal(root)
print_tree(root, node_list)
