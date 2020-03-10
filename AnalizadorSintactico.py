from math import *

from AnalizadorLexico import *
from GeneradorAutomatas import GeneradorAFN

class AnalizadorSintacticoCalculadora():

    def __init__(self, lexico):
        self._lexico = lexico
        self._generador = GeneradorAFN()

    def analizar(self):
        resultado = 0
        analisisValido,resultado = self.E(resultado)

        if analisisValido:
            #Se verifica que todos los caracteres de la cadena hayan sido analizados
            if self._lexico.getToken() != 0:
                analisisValido = False

        return (analisisValido,resultado)

    def E(self,resultado):
        valido, resultado = self.T(resultado)
        if valido:
            valido, resultado = self.Ep(resultado)
            if valido:
                return (True,resultado)

        return (False,resultado)

    def Ep(self,resultado):
        token = self._lexico.getToken()
        resultado2 = 0

        if token >= 0:
            if token == TokenCalculadora.SUMA:
                valido, resultado2 = self.T(resultado2)
                if valido:
                    resultado += resultado2

                    valido, resultado = self.Ep(resultado)
                    if valido:
                        return (True,resultado)
                return (False,resultado)

            elif token == TokenCalculadora.RESTA:
                valido, resultado2 = self.T(resultado2)
                if valido:
                    resultado -= resultado2
                    
                    valido, resultado = self.Ep(resultado)
                    if valido:
                        return (True,resultado)
                return (False,resultado)

        else:
            return (False,resultado)

        if token > 0:
            self._lexico.rewind()
        return (True,resultado)

    def T(self,resultado):
        valido, resultado = self.C(resultado)
        if valido:
            valido, resultado = self.Tp(resultado)
            if valido:
                return (True,resultado)
                
        return (False,resultado)

    def Tp(self,resultado):
        token = self._lexico.getToken()
        resultado2 = 0

        if token >= 0:
            if token == TokenCalculadora.MULTIPLICACION:
                valido, resultado2 = self.C(resultado2)
                if valido:
                    resultado *= resultado2
                    
                    valido, resultado = self.Tp(resultado)
                    if valido:
                        return (True,resultado)
                return (False,resultado)

            if token == TokenCalculadora.DIVISION:
                valido, resultado2 = self.C(resultado2)
                if valido:
                    try:
                        resultado /= resultado2
                    except Exception as e:
                        print(e)
                        return (False,resultado)

                    valido, resultado = self.Tp(resultado)
                    if valido:
                        return (True,resultado)
                return (False,resultado)
        else:
            return (False,resultado)

        if token > 0:
            self._lexico.rewind()
        return (True,resultado)

    def C(self,resultado):
        valido, resultado = self.F(resultado)
        if valido:
            valido, resultado = self.Cp(resultado)
            if valido:
                return (True,resultado)
                
        return (False,resultado)

    def Cp(self,resultado):
        token = self._lexico.getToken()
        resultado2 = 0

        if token >= 0:
            if token == TokenCalculadora.POTENCIA:
                valido, resultado2 = self.F(resultado2)
                if valido:
                    resultado **= resultado2

                    valido, resultado = self.Cp(resultado)
                    if valido:
                        return (True,resultado)
                return (False,resultado)

        else:
            return (False,resultado)

        if token > 0:
            self._lexico.rewind()
        return (True,resultado)

    def F(self,resultado):
        token = self._lexico.getToken()

        if token >= 0:

            if token == TokenCalculadora.NUMERO:
                resultado = float(self._lexico.getUltimoLexemaValido())
                return (True,resultado)

            elif token == TokenCalculadora.PI:
                resultado = pi
                return (True,resultado)

            elif token == TokenCalculadora.EXPONENCIAL:
                resultado = e
                return (True,resultado)

            elif token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                valido, resultado = self.E(resultado)
                if valido:
                    token = self._lexico.getToken()

                    if token == TokenCalculadora.AGRUPADOR_DERECHO:
                        return (True,resultado)

                return (False,resultado)

            elif token == TokenCalculadora.SENO:
                token = self._lexico.getToken()

                if token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                    valido, resultado = self.E(resultado)
                    if valido:
                        resultado = sin(resultado)

                        token = self._lexico.getToken()
                        if token == TokenCalculadora.AGRUPADOR_DERECHO:
                            return (True,resultado)

                return (False,resultado)

            elif token == TokenCalculadora.COSENO:
                token = self._lexico.getToken()

                if token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                    valido, resultado = self.E(resultado)
                    if valido:
                        resultado = cos(resultado)

                        token = self._lexico.getToken()
                        if token == TokenCalculadora.AGRUPADOR_DERECHO:
                            return (True,resultado)

                return (False,resultado)

            elif token == TokenCalculadora.TANGENTE:
                token = self._lexico.getToken()

                if token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                    valido, resultado = self.E(resultado)
                    if valido:
                        resultado = tan(resultado)

                        token = self._lexico.getToken()
                        if token == TokenCalculadora.AGRUPADOR_DERECHO:
                            return (True,resultado)

                return (False,resultado)

            elif token == TokenCalculadora.LOGARITMO_NATURAL:
                token = self._lexico.getToken()

                if token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                    valido, resultado = self.E(resultado)
                    if valido:
                        resultado = log(resultado)

                        token = self._lexico.getToken()
                        if token == TokenCalculadora.AGRUPADOR_DERECHO:
                            return (True,resultado)

                return (False,resultado)

            elif token == TokenCalculadora.LOGARITMO:
                token = self._lexico.getToken()
                if token == TokenCalculadora.NUMERO:
                    base = float(self._lexico.getUltimoLexemaValido())

                    token = self._lexico.getToken()
                    if token == TokenCalculadora.AGRUPADOR_IZQUIERDO:
                        valido, resultado = self.E(resultado)
                        if valido:
                            resultado = log(resultado,base)

                            token = self._lexico.getToken()
                            if token == TokenCalculadora.AGRUPADOR_DERECHO:
                                return (True,resultado)

                    return (False,resultado)    

            return (False,resultado)

        else:
            return (False,resultado)

        if token > 0:
            self._lexico.rewind()
        return (True,resultado)

class TokenCalculadora(object):

    #Constantes referentes a los token de las ER
    SUMA = 10

    RESTA = 20

    MULTIPLICACION = 30

    DIVISION = 40

    POTENCIA = 50

    SENO = 60

    COSENO = 70

    TANGENTE = 80

    AGRUPADOR_IZQUIERDO= 90

    AGRUPADOR_DERECHO = 91

    NUMERO = 100

    PI = 110

    EXPONENCIAL = 120

    LOGARITMO_NATURAL = 130

    LOGARITMO = 140