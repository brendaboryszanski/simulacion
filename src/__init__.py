from src.functions import menor_tps
from src.global_variables import VariablesGlobales
from src.rama_llegada import *
from src.rama_salida import *

def empezar_simulacion(ctx):
    indice_menor_tps = menor_tps(ctx)
    if ctx.TPLL <= ctx.TPS[indice_menor_tps]:
        ejectutar_rama_llegada(ctx)
    else:
        ejecutar_rama_salida(ctx, indice_menor_tps)

def obtenerNumero(mensaje):
    print(mensaje)
    number = "sin valor"
    while not number.isdigit():
        number = input()
        if not number.isdigit():
            print("Debe ingresar un numero entero")
    return int(number)


if __name__ == '__main__':
    cantidad_operadores = obtenerNumero("Ingrese cantidad de operadores")
    maximo_en_cola = obtenerNumero("Ingrese numero de personas por limite en la cola")

    variables_globales = VariablesGlobales(cantidad_operadores, maximo_en_cola)
    empezar_simulacion(variables_globales)

