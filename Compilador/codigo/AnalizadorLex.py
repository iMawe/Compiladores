import ply.lex as lex
import sys


reservadas = {
    'uma' : 'uma',
    'hun' : 'hun',
    'chillu' : 'chillu',
    'chaya' : 'chaya',
    'unan' : 'unan',
    'ari' : 'ari',
    'shuc' : 'shuc',
    'pacha' : 'pacha',
    'haykaq' : 'haykaq'
    }
#     'UMA', ##MAIN
#     'HUNTA', ##int
#     'CHILLU', ##BOOL
#     'CHAYA', ##RETURN
#     'UNAN', ##FUNCTION //planteamiemto
#     'ARI', ##if
#     'SHUC' ##else
#     'PACHA', ##while
#     'HAYKAQ', ##for



tokens = [
    'num',
    'boolean',
    'opemasmas',
    'opesuma',
    'opemenos',
    'opemult',
    'opediv',
    'opemod',
    'igualq',
    'noigualq',
    'menorq',
    'menoriguq',
    'mayorq',
    'mayoiguq',
    'parenl',
    'parenr',
    'and',
    'or',
    'assign',
    'keyl',
    'keyr',
    'id',
    'comma',
    'dotcomma',
] + list(reservadas.values())

#  'MAYORQ', #GT
#     'MAYOIGUQ',#GTE
#     'MENORQ', #LT
#     'MENOIGUQ', #LTE
#     'NOIGUALQ', #NE

#tokens = tokens+reservadas

t_ignore     = " \t" # Caracteres ignorados
t_opemasmas  = r'\+\+'
t_opesuma    = r'\+'
t_opemenos   = r'\-'
t_opemult    = r'\*'
t_opediv     = r'/'
t_opemod     = r'%'
t_and        = r'&'
t_or         = r'\|'
t_assign     = r'='
t_igualq     = r'=='
t_noigualq   = r'<>'
t_menorq     = r'<'
t_menoriguq   = r'<='
t_mayorq     = r'>'
t_mayoiguq   = r'>='
t_parenl     = r'\('
t_parenr     = r'\)'
t_keyl       = r'\{'
t_keyr       = r'\}'
t_comma      = r'\,'
t_dotcomma   = r'\;'

 # A regular expression rule with some action code
def t_num(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema  
    return t

def t_boolean(t):
    r'true | false'
    return t

def t_id(t):
    r'[a-zA-Z]+ ( [a-zA-Z0-9]* )'    
    t.type = reservadas.get(t.value,'id')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

def get_tokens(file):
    tokens = []
    # Build the lexer
    

    # Test it out

    #f = open("test/ex3.c", "r")
    f = open(file, "r")
    data = f.read()

    # Give the lexer some input
    lexer.input(data)
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        #print(tok)
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)
        #print( str(tok.type) + ' ', end='' )
        tokens.append( [tok.type, tok.value, tok.lineno] )

    return tokens

if __name__ == "__main__":
    tokens = get_tokens( sys.argv[1])
    for tok in tokens:
        print( str(tok[0]) + ' ', end='')
    print()

    print(tokens)