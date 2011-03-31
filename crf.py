#!/usr/bin/python

import sys
import ply.lex as lex
import lextokens
from rangefunctions import *

# Build the lexer
lex.lex(module=lextokens)

tokens = lextokens.tokens

names = {}
maxnames = {}

def p_program_definition(t):
	'program : definition program'
	t[0] = t[1] + t[2]

def p_program_assignment(t):
	'program : assignment program'
	t[0] = t[1] + t[2]

def p_program_empty(t):
	'program : empty'
	t[0] = ""

def p_definition(t):
	'definition : INT NAME SEMICOLON range'
	t[0] = "int %s; %s\n" % (t[2], t[4][0])
	names[t[2]] = t[4][1]

def p_empty(t):
	'empty : '
	pass

def p_range_nostep(t):
	'range : RANGEBEGIN NUMBER MINUS NUMBER RANGESTOP'
	t[0] = ("/*[%d-%d|%d]*/" % (t[2], t[4], 1),
			(int(t[2]), int(t[4]), 1))

def p_range(t):
	'range : RANGEBEGIN NUMBER MINUS NUMBER BAR NUMBER RANGESTOP'
	t[0] = ("/*[%d-%d|%d]*/" % (t[2], t[4], t[6]),
			(int(t[2]), int(t[4]), int(t[6])))

def p_prange_e(t):
	'range : empty'
	t[0] = ("", (-sys.maxint, sys.maxint, 1))

def p_assignment(t):
	'assignment : NAME EQUALS expression SEMICOLON'
	names[t[1]] = t[3][1]
	if maxnames.has_key(t[1]):
		ma = maxnames[t[1]]
		ma[0] = max(ma[0], t[3][1][0])
		ma[1] = max(ma[1], t[3][1][1])
		maxnames[t[1]] = ma
	else:
		maxnames[t[1]] = t[3][1]

	t[0] = "%s = %s; /*[%d-%d|%d]*/\n" % ((t[1], t[3][0]) + t[3][1])

def p_assignment_c(t):
	'''assignment : NAME PLUSEQ expression SEMICOLON
	            | NAME DIVEQ expression SEMICOLON
	            | NAME MULEQ expression SEMICOLON
	            | NAME LEFTEQUALS expression SEMICOLON
	            | NAME RIGHTEQUALS expression SEMICOLON'''
	l = names[t[1]]
	r = t[3][1]

	if t[2] == "+=":
		out = range_plus(l, r)
	elif t[2] == "<<=":
		out = range_left(l, r)
	elif t[2] == "/=":
		out = range_div(l, r)
	elif t[2] == "*=":
		out = range_mul(l, r)
	elif t[2] == ">>=":
		out = range_right(l, r)

	names[t[1]] = out

	if maxnames.has_key(t[1]):
		ma = maxnames[t[1]]
		ma  = (min(ma[0], out[0]), max(ma[1], out[1]), 0)
		maxnames[t[1]] = ma
	else:
		maxnames[t[1]] = out

	t[0] = "%s %s %s; /*[%d-%d|%d]*/\n" % ((t[1], t[2], t[3][0]) + out)

def p_expression_plus(t):
	'expression : expression PLUS expression'
	t[0] = ("(%s) + (%s)" % (t[1][0], t[3][0]),
			range_plus(t[1][1], t[3][1]))

def p_expression_minus(t):
	'expression : expression MINUS expression'
	t[0] = ("(%s) - (%s)" % (t[1][0], t[3][0]),
			range_minus(t[1][1], t[3][1]))

def p_expression_mul(t):
	'expression : expression TIMES expression'
	t[0] = ("(%s) * (%s)" % (t[1][0], t[3][0]),
			range_mul(t[1][1], t[3][1]))

def p_expression_div(t):
	'expression : expression DIVIDE expression'
	t[0] = ("(%s) / (%s)" % (t[1][0], t[3][0]),
			range_div(t[1][1], t[3][1]))

def p_expression_left(t):
	'expression : expression LEFT expression'
	t[0] = ("(%s) << (%s)" % (t[1][0], t[3][0]),
			range_left(t[1][1], t[3][1]))

def p_expression_right(t):
	'expression : expression RIGHT expression'
	t[0] = ("(%s) >> (%s)" % (t[1][0], t[3][0]),
			range_right(t[1][1], t[3][1]))

def p_expression_paren(t):
	'expression : LPAREN expression RPAREN'
	t[0] = ("(%s)" % t[2][0],
			t[2][1])

def p_expression_num(t):
	'expression : NUMBER'
	t[0] = ("%s" % t[1],
			(int(t[1]), int(t[1]), 1))

def p_expression_negnum(t):
	'expression : MINUS expression'
	t[0] = ("(-(%s))" % t[2][0],
			(-t[2][1][1], -t[2][1][0], t[2][1][2]))


def p_expression_name(t):
	'expression : NAME'
	t[0] = ("%s" % t[1],
			names[t[1]])

def p_error(t):
	print "error: ", t

import ply.yacc as yacc
yacc.yacc()

import sys
if len(sys.argv) == 1:
	program = """
int x; /*[0-65535]*/
int y; /*[0-65535]*/
int z;

z = x << 10;
y *= 2;
z += y;
"""
else:
	program = open(sys.argv[1]).read()

print yacc.parse(program)

for name, range in maxnames.items():
	import math
	lmin = abs(range[0])
	lmax = abs(range[1])
	if lmin != 0:
		lmin = (math.log(lmin, 2) + 1)
	if lmax != 0:
		lmax = (math.log(lmax, 2) + 1)
	print "%s\t: %15d to %15d, width: %d" % (name, range[0], range[1], max(lmin, lmax))
