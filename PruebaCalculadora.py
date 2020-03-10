from AnalizadorLexico import *
from AnalizadorSintactico import *
from GeneradorAutomatas import *

import sys

cadena = sys.argv[1]

tabular = ManejadorTabulares.recuperarTabular('TabularCalculadora.dat')

automata = ManejadorTabulares.generarAFDDeTabular(tabular)

automata.imprimirAutomata()

#print(automata.getEstadoInicial().getEstadosTransicion('5')[0].getNombre())

lexico = AnalizadorLexico(automata, cadena)

sintactico = AnalizadorSintacticoCalculadora(lexico)

resultado = -1

valido,resultado = sintactico.analizar()

if valido:
	print('Resultado:',resultado)
else:
	print('Error')