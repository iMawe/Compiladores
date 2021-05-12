import ply.lex as lex
import os
import sys

reservadas = {
    'uma' : 'uma', ##main
    'liwry' : 'liwry', ##imprimir
    'pacha' : 'pacha', ##while
    'ari' : 'ari', ##if
    'chay' : 'chay', ##for
    'wall' : 'wall', ##range
    'pak' : 'pak', ##break
    'llawi' : 'llawi', ##switch
    'chaya' : 'chaya', ##return
    'bool' : 'bool', ##bool
    'null' : 'null',
    'shuc' : 'shuc' ##else
}

tokens  = [
    'numeros',
    'boolean',
    'opesuma',
    'opemenos',
    'opemult',
    'opediv',
    'opemod',
    'opedivint',
    'parenl',
    'parenr',
    'and',
    'or',
    'assign',
    'llavl',
    'llavr',
    'id',
    'coma',
    'mayorq',
    'igualq',
    'noigualq',
    'menorq',
    'decimal',
    'entero',
    'cadena'
] + list(reservadas.values())

# Tokens
t_coma       = r'\,'
t_llavl      = r'\{'
t_llavr      = r'\}'
t_parenl     = r'\('
t_parenr     = r'\)'
t_and        = r'&'
t_or         = r'\|'
t_assign     = r'='
t_opesuma    = r'\+'
t_opemenos   = r'-'
t_opemult    = r'\*'
t_opediv     = r'/'
t_opemod     = r'%'
t_opedivint  = r'//'
t_menorq     = r'<'
t_mayorq     = r'>'
t_igualq     = r'=='
t_noigualq   = r'!='

def t_boolean(t):
    r'true| false'
    return t

def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_id(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'id')    # Check for reserved words
     return t

def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /# .. #/
def t_comen_multilinea(t):
    r'/\#(.|\n)*?\#/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple ## ...
def t_comen_simple(t):
    r'\#\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico

lexer = lex.lex()

def get_tokens(file):
    tokens = []
    f = open(file, "r")
    data = f.read()
    # Give the lexer some input
    lexer.input(data)


# archivo = open('codigo.txt', 'r')
# contenido = archivo.read()

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        #print(tok)
        tokens.append( [tok.type, tok.value, tok.lineno] )
    return tokens

if __name__ == "__main__":
    tokens = get_tokens(sys.argv[1])
    for tok in tokens:
        print(str(tok[0]) + ' ', end='')
    print()
    print(tokens)
