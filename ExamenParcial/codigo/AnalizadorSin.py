import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from sys import stdin
from AnalizadorSem import *

precedence = (
	('right', 'ID','WAQYAY','QALLARIY','ARI','PACHA'),
    ('right', 'UNANCHALLIKU'),
    ('right', 'UJJINA'),
    ('right', 'ASSIGN'),
    ('right', 'UPDATE'),
    ('left', 'NOIGUALQ'),
    ('left', 'MAYORQ','MAYOIGUQ','MENORQ','MENOIGUQ'),
    ('left', 'OPESUMA','OPEMENOS'),
    ('left', 'OPEMULT','OPEDIV'),
    ('right', 'OPEODD'),
    ('left', 'PARENL','PARENR'),
	)

def p_program(p):
	'''program : block'''
	#print "program"
	p[0] = program(p[1],"Program")

def p_block(p):
	'''block : sapaDecl ujjDecl unanDecl statement'''
	p[0] = block(p[1],p[2],p[3],p[4],"Block")
	#print "block"

def p_sapaDecl(p):
	'''sapaDecl : SAPAKUTIN sapaAssignmentList SEMMICOLOM'''
	p[0] = sapaDecl(p[2],"sapaDecl")
	#print "sapaDecl"

def p_sapaDeclEmpty(p):
	'''sapaDecl : empty'''
	p[0] = Null()
	#print "nulo"

def p_sapaAssignmentList1(p):
	'''sapaAssignmentList : ID ASSIGN NUMEROS'''
	p[0] = sapaAssignmentList1(Id(p[1],p.lineno(1),"Variable"),Assign(p[2],p.lineno(2),"Operador"),Numeros(p[3],p.lineno(3),"Numero"),"SapaAssignmentList1")
	#print "sapaAssignmentList 1"

def p_sapaAssignmentList2(p):
	'''sapaAssignmentList : sapaAssignmentList COMMA ID ASSIGN NUMEROS'''
	p[0] = sapaAssignmentList2(p[1],Id(p[3],p.lineno(3),"Variable"),Assign(p[4],p.lineno(4),"Operador"),Numeros(p[5],p.lineno(5),"Numero"),"SapaAssignmentList2")
	#print "sapaAssignmentList 2"

def p_ujjDecl1(p):
	'''ujjDecl : UJJINA identList SEMMICOLOM'''
	p[0] = ujjDecl1(p[2],"ujjDecl1")
	#print "ujjDecl 1"

def p_ujjDeclEmpty(p):
	'''ujjDecl : empty'''
	p[0] = Null()
	#print "nulo"

def p_identList1(p):
	'''identList : ID'''
	p[0] = identList1(Id(p[1],p.lineno(1),"Variable"),"identList1")
	#print "identList 1"

def p_identList2(p):
	'''identList : identList COMMA ID'''
	p[0] = identList2(p[1],Id(p[3],p.lineno(3),"Variable"),"identList2")
	#print "identList 2"

def p_unanDecl1(p):
	'''unanDecl : unanDecl UNANCHALLIKU ID SEMMICOLOM block SEMMICOLOM'''
	p[0] = unanDecl1(p[1],Id(p[3],p.lineno(1),"Funcion"),p[5],"unanDecl1")
	#print "unanDecl 1"

def p_unanDeclEmpty(p):
	'''unanDecl : empty'''
	p[0] = Null()
	#print "nulo"

def p_statement1(p):
	'''statement : ID UPDATE expression'''
	p[0] = statement1(Id(p[1],p.lineno(1),"Variable"),Update(p[2],p.lineno(2), "Operador"),p[3],"statement1")
	#print "statement 1"

def p_statement2(p):
	'''statement : WAQYAY ID'''
	p[0] = statement2(Id(p[2],p.lineno(2),"Variable"),"statement2", p.lineno(1), "Funcion")
	#print "statement 2"

def p_statement3(p):
	'''statement : QALLARIY statementList TUKUKUY'''
	p[0] = statement3(p[2],"statement3", p.lineno(1), "Funcion")
	#print "statement 3"

def p_statement4(p):
	'''statement : ARI condition HINASPA statement'''
	p[0] = statement4(p[2],p[4],"statement4", p.lineno(1), "Funcion")
	#print "statement 4"

def p_statement5(p):
	'''statement : PACHA condition RURAY statement'''
	p[0] = statement5(p[2],p[4],"statement5", p.lineno(1), "Funcion")
	#print "statement 5"

def p_statementEmpty(p):
	'''statement : empty'''
	p[0] = Null()
	#print "nulo"

def p_statementList1(p):
	'''statementList : statement'''
	p[0] = statementList1(p[1],"statementList1")
	#print "statementList 1"

def p_statementList2(p):
	'''statementList : statementList SEMMICOLOM statement'''
	p[0] = statementList2(p[1],p[3],"statementList2")
	#print "statementList 2"

def p_condition1(p):
	'''condition : OPEODD expression'''
	p[0] = condition1(p[2],"condition1")
	#print "condition 1"

def p_condition2(p):
	'''condition : expression relation expression'''
	p[0] = condition2(p[1],p[2],p[3],"condition2")
	#print "condition 2"

def p_relation1(p):
	'''relation : ASSIGN'''
	p[0] = relation1(Assign(p[1],p.lineno(1),"Operador"),"relation1")
	#print "relation 1"

def p_relation2(p):
	'''relation : NOIGUALQ'''
	p[0] = relation2(Noigualq(p[1],p.lineno(1),"Operador"),"relation2")
	#print "relation 2"

def p_relation3(p):
	'''relation : MENORQ'''
	p[0] = relation3(Menorq(p[1],p.lineno(1),"Operador"),"relation3")
	#print "relation 3"

def p_relation4(p):
	'''relation : MAYORQ'''
	p[0] = relation4(Mayorq(p[1],p.lineno(1),"Operador"),"relation4")
	#print "relation 4"

def p_relation5(p):
	'''relation : MENOIGUQ'''
	p[0] = relation5(Menoiguq(p[1],p.lineno(1),"Operador"),"relation5")
	#print "relation 5"

def p_relation6(p):
	'''relation : MAYOIGUQ'''
	p[0] = relation6(Mayoiguq(p[1],p.lineno(1),"Operador"),"relation6")
	#print "relation 6"

def p_expression1(p):
	'''expression : term'''
	p[0] = expression1(p[1],"expression1")
	#print "expresion 1"

def p_expression2(p):
	'''expression : addingOperator term'''
	p[0] = expression2(p[1],p[2],"expression2")
	#print "expresion 2"

def p_expression3(p):
	'''expression : expression addingOperator term'''
	p[0] = expression3(p[1],p[2],p[3],"expression3")
	#print "expresion 3"

def p_addingOperator1(p):
	'''addingOperator : OPESUMA'''
	p[0] = addingOperator1(Opesuma(p[1],p.lineno(1),"Operador"),"addingOperator")
	#print "addingOperator 1"

def p_addingOperator2(p):
	'''addingOperator : OPEMENOS'''
	p[0] = addingOperator2(Operesta(p[1],p.lineno(1),"Operador"),"subtractionOperator")
	#print "addingOperator 1"

def p_term1(p):
	'''term : factor'''
	p[0] = term1(p[1],"term1")
	#print "term 1"

def p_term2(p):
	'''term : term multiplyingOperator factor'''
	p[0] = term2(p[1],p[2],p[3],"term2")
	#print "term 1"

def p_multiplyingOperator1(p):
	'''multiplyingOperator : OPEMULT'''
	p[0] = multiplyingOperator1(Opemult(p[1],p.lineno(1),"Operador"),"multiplyingOperator")
	#print "multiplyingOperator 1"

def p_multiplyingOperator2(p):
	'''multiplyingOperator : OPEDIV'''
	p[0] = multiplyingOperator2(Opediv(p[1],p.lineno(1),"Operador"),"divisiongOperator")
	#print "multiplyingOperator 2"

def p_factor1(p):
	'''factor : ID'''
	p[0] = factor1(Id(p[1],p.lineno(1),"Variable"),"factor1")
	#print "factor 1"

def p_factor2(p):
	'''factor : NUMEROS'''
	p[0] = factor2(Numeros(p[1],p.lineno(1),"Numero"),"factor2")
	#print "factor 1"

def p_factor3(p):
	'''factor : PARENL expression PARENR'''
	p[0] = factor3(p[2],"factor3")
	#print "factor 1"

def p_empty(p):
	'''empty :'''
	pass

def p_error(p):
	print ("Error de sintaxis ", p)
	#print "Error en la linea "+str(p.lineno)

def buscarFicheros(directorio):
	ficheros = []
	numArchivo = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk(directorio):
		ficheros.append(files)

	for file in files:
		print (str(cont)+". "+file)
		cont = cont+1

	while respuesta == False:
		numArchivo = input('\nNumero del test: ')
		for file in files:
			if file == files[int(numArchivo)-1]:
				respuesta = True
				break

	print ("Has escogido \"%s\"" %files[int(numArchivo)-1])

	return files[int(numArchivo)-1]

def traducir(result):
	graphFile = open('graphviztrhee.vz','w')
	graphFile.write(result.traducir())
	graphFile.close()
	print ("El programa traducido se guardo en \"graphviztrhee.vz\"")

directorio = 'C:/Users/User/Desktop/Python/test/'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

yacc.yacc()
result = yacc.parse(cadena,debug=1)

#result.imprimir(" ")
#print result.traducir()
traducir(result)



#print result

