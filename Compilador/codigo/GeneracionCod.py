from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree, update_stack
from AnalizadorSem import findVal
import sys
import pandas as pd

file_out = open ("code.s","w")

def genera_assembler(root):
    file_out.write(".data\n")
    crea_variable(root)#escribe cada variable
    file_out.write(".text\nmain:\n")
    generar_assing(root)
    file_out.write("\n \tjr $ra ")

def crea_variable (node):
    if node.symbol.symbol == "TYPE":
        escribe_id (node.father.children[1].children[0])#va al derecho
        
    for child in node.children:
        crea_variable(child)

def escribe_id (node):#en el archivo de salida escribe var y lo demas , node es como se llama la varibale
   file_out.write("\tvar_" + str(node.lexeme) + ": .word 0:1\n")

def generar_assing(node):
    if node.symbol.symbol == "assign":
        #print("sign")
        node_e=node.father.children[2]
        node_id=node.father.children[0]
        generar_exprT(node_e.children[0])
        generar_exprE_prima(node_e.children[1])
        file_out.write("\n\tla  $t1, var_"+ str(node_id.lexeme)+ "\n"+"\tsw  $a0, 0($t1)\n")
        #registrar_operandos(node)#tiene que ir en un for pero cuando lo pongo me sale fallas
    for child in node.children:
        generar_assing(child)

def final_var(node):
     if node.symbol.symbol == "TYPE":
        node_var=node.father.children[1].children[0]
        file_out.write("\tla  $t1, var_"+ str(node_var.lexeme)+ "\n"+"\tsw  $a0, 0($t1)")
     for child in node.children:#solo funciona para un caso en particular, si pongo mas variables me las muestra todas 
         final_var(child)
def print_var(node):
      file_out.write("\nla  $t1, var_"+ str(node.lexeme)+ "\n"+"sw  $a0, 0($t1)")

def generar_expr(node):
     if node.symbol.symbol == "E":
        #escribe_num(node.children[0])
        #print("encontrando node:",node.symbol.symbol)
        generar_exprT(node.children[0])
        generar_exprE_prima(node.children[1])
        #registrar_operandos(node)#tiene que ir en un for pero cuando lo pongo me sale fallas
     for child in node.children:
        generar_expr(child)

def generar_exprT(node):
    print(node.symbol.symbol)
    if node.children[0].symbol.symbol=="TERM":
        #print("genero codigo para term")
        generar_terminal(node.children[0])
    elif node.children[0].symbol.symbol=="parenl":
        print()
        #print("genero parenl")
def generar_terminal(node):
    if node.children[0].symbol.symbol=="num":
        file_out.write("\tli"+ " $a0,"+ str(node.children[0].lexeme)+ "\n")
        #print("num")
    elif node.children[0].symbol.symbol=="id":#buscar en la tabla de simbolo cuanto vale
        #print("id")
        crea_variable (node)
    elif node.children[0].symbol.symbol== 'boolean':
        #print("Booleano encontrado...")
        generar_bool(node)
        #print("encontre un boolean")#true 1 y false 0

def generar_bool(node):
    if node.children[0].lexeme == "true":
        file_out.write("\tli"+ " $a0,"+ "1 "+"\n")
    elif node.children[0].lexeme == "false":
        file_out.write("\tli"+ " $a0,"+ "0 "+"\n")  

def generar_exprE_prima(node):
    print(node.symbol.symbol)
    if len(node.children)>1:
        file_out.write("\tsw " +" $a0 "+" 0($sp)\n")
        file_out.write("\taddiu  $sp  $sp-4\n\n")
        generar_exprT(node.children[1])
        file_out.write(" \tlw $t1 4($sp)\n")
        if node.children[0].children[0].symbol.symbol=="opesuma":
                file_out.write("\tadd $a0, $a0, $t1")
        elif node.children[0].children[0].symbol.symbol=="opemenos":
                file_out.write("\tsub $a0, $a0, $t1")
        elif node.children[0].children[0].symbol.symbol=="opemult":
                file_out.write("\tmul $a0, $a0, $t1")
        elif node.children[0].children[0].symbol.symbol=="opediv":
                file_out.write("\tdiv $a0, $a0, $t1")  
                file_out.write("\n\tmflo $a0")
        elif  node.children[0].children[0].symbol.symbol=="opemod":
               file_out.write("\tdiv $t1 $a0") 
               file_out.write("\tmfhi $a0")
        elif node.children[0].children[0].symbol.symbol=="igualq":
               file_out.write("\n \taddiu $sp $sp 4\n")
        elif node.children[0].children[0].symbol.symbol=="noigualq":
               file_out.write("\n \taddiu $sp $sp 4\n")
        elif node.children[0].children[0].symbol.symbol=="mayorq":
               file_out.write("\n \tbge $t1, $t2,\n")
        elif node.children[0].children[0].symbol.symbol=="mmenorq":
               file_out.write("\n \tble $t2, $t1,\n")
        file_out.write("\n \taddiu $sp $sp 4\n")
        #print("mas de 1")
        generar_exprE_prima(node.children[2])

     
if __name__ == "__main__":
    file_name=sys.argv[0]

    #lexer
    tokens = get_tokens (file_name)
    tokens.append (['$', None, None])
    
    #analizador sintatico
    root, node_list = parser(tokens)
    #analizador semantico
    #buscar_if_else(root)
    findVal(root)#check_nodes(root)
    #set_types(root)
    #code generation
    genera_assembler(root)
    file_out.close()

    #print_tree(root, node_list, True)
    #print symbol_table()

    #FALTA EL ID: buscar generarexprT,buscar cuanto vale en la tabla de simbolos Y EL BOLEEAN