import ply.lex as lex

reserved = {
		'int': 'INT'
		}

tokens = (
		'NAME', 'NUMBER',
		'PLUS','MINUS','TIMES','DIVIDE',
		'EQUALS', 'PLUSEQ', 'RIGHTEQUALS', 'LEFTEQUALS', 'DIVEQ', 'MULEQ',
		'LPAREN','RPAREN',
		'SEMICOLON', 'BAR', 'RANGEBEGIN', 'RANGESTOP', 'LEFT', 'RIGHT'
		) + tuple(reserved.values())

t_PLUSEQ = r'\+='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_BAR = r'\|'
t_RANGEBEGIN = r'/\*\['
t_RANGESTOP = r'\]\*/'
t_LEFT = r'<<'
t_RIGHT = r'>>'
t_LEFTEQUALS = r'<<='
t_RIGHTEQUALS = r'>>='
t_DIVEQ = r'/='
t_MULEQ = r'\*='

NAME=r'[a-zA-Z_][a-zA-Z0-9_]*'
NUMBER=r'\d+'

@lex.TOKEN(NAME)
def t_NAME(t):
	t.type = reserved.get(t.value, 'NAME')
	return t

@lex.TOKEN(NUMBER)
def t_NUMBER(t):
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

# Ignored characters
t_ignore = " \t" 

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def t_comment(t):
    r'(/\*[^\[](.|\n)*?\*/)|(//.*)'
    pass
