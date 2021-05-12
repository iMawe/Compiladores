import ply.lex as lex
import re
import codecs
import os
import sys

reservadas = ['QALLARIY','TUKUKUY','ARI','HINASPA','PACHA','RURAY','WAQYAY','SAPAKUTIN','UJJINA','UNANCHALLIKU','CHAYA','HAYKUY','SHUC']
#     'QALLARIY', ##BEGIN
#     'TUKUKUY', ##END
#     'ARI', ##if
#     'HINASPA', ##then
#     'PACHA', ##while
#     'RURAY', ##do
#     'WAQYAY', ##call
#     'SAPAKUTIN', ##const
#     'UJJINA', ##var
#     'UNANCHALLIKU', ##procedure
#     'CHAYA', ##return  OUT
#     'HAYKUY', ##IN
#     'SHUC' ##else
tokens = reservadas+['ID','NUMEROS','OPESUMA','OPEMENOS','OPEMULT','OPEDIV','OPEODD','ASSIGN','NOIGUALQ','MENORQ','MENOIGUQ','MAYORQ','MAYOIGUQ','PARENL','PARENR','COMMA','SEMMICOLOM','DOT','UPDATE','DECIMAL','ENTERO','CADENA']
#  'MAYORQ', #GT
#     'MAYOIGUQ',#GTE
#     'MENORQ', #LT
#     'MENOIGUQ', #LTE
#     'NOIGUALQ', #NE

#tokens = tokens+reservadas

# reservadas = {
	# 'begin':'BEGIN',
	# 'end':'END',
	# 'if':'IF',
	# 'then':'THEN',
	# 'while':'WHILE',
	# 'do':'DO',
	# 'call':'CALL',
	# 'const':'CONST',
	# 'int':'VAR',
	# 'procedure':'PROCEDURE',
	# 'out':'OUT',
	# 'in':'IN',
	# 'else':'ELSE'
# }

#tokens = tokens+list(reservadas.values())

t_ignore     = " \t" # Caracteres ignorados
t_OPESUMA    = r'\+'
t_OPEMENOS   = r'\-'
t_OPEMULT    = r'\*'
t_OPEDIV     = r'/'
t_OPEODD     = r'ODD'
t_ASSIGN     = r'='
t_NOIGUALQ   = r'<>'
t_MENORQ     = r'<'
t_MENOIGUQ   = r'<='
t_MAYORQ     = r'>'
t_MAYOIGUQ   = r'>='
t_PARENL     = r'\('
t_PARENR     = r'\)'
t_COMMA      = r','
t_SEMMICOLOM = r';'
t_DOT        = r'\.'
t_UPDATE     = r':='

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value.upper() in reservadas:
		t.value = t.value.upper()
		#reservadas.get(t.value,'ID')
		t.type = t.value

	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

#dsfjksdlgjklsdgjsdgslxcvjlk-,.
def t_COMMENT(t):
	r'\#.*'
	pass

# Comentario de múltiples líneas /# .. #/
def t_COMEN_MULTILINEA(t):
    r'/\#(.|\n)*?\#/'
    t.lexer.lineno += t.value.count('\n')

def t_NUMEROS(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_error(t):
	print ("caracter ilegal '%s'" % t.value[0])
	t.lexer.skip(1)

# def buscarFicheros(directorio):
# 	ficheros = []
# 	numArchivo = ''
# 	respuesta = False
# 	cont = 1

# 	for base, dirs, files in os.walk(directorio):
# 		ficheros.append(files)

# 	for file in files:
# 		print str(cont)+". "+file
# 		cont = cont+1

# 	while respuesta == False:
# 		numArchivo = raw_input('\nNumero del test: ')
# 		for file in files:
# 			if file == files[int(numArchivo)-1]:
# 				respuesta = True
# 				break

# 	print "Has escogido \"%s\" \n" %files[int(numArchivo)-1]

# 	return files[int(numArchivo)-1]

# directorio = '/Users/sebas/Documents/Compiladores/pl0/analizador version 1/test/'
# archivo = buscarFicheros(directorio)
# test = directorio+archivo
# fp = codecs.open(test,"r","utf-8")
# cadena = fp.read()
# fp.close()

analizador = lex.lex()

#analizador.input(cadena)

# while True:
# 	tok = analizador.token()
# 	if not tok : break
# 	print tok