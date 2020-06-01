import random
import math
import sys

sys.setrecursionlimit(1500)


### START FDPS ###
# IA: Intervalo entre arribo de llamados de clientes all call-center en minutos
def ia():
    random = generar_random_con_restriccion(0)
    return (2.2529/((1/random-1)**(1/5))+5)/60


# TAI: TIempo de atencion de producto individual en minutos.
def tai():
    random = generar_random_con_restriccion(1, 0)
    return (2.0029/((1/random-1)**(1/418.0000))+418.0000)/60


# TAP: Tiempo de atencion de paquete en minutos. 
def tap():
    random = generar_random_con_restriccion(1, 0)
    return (2.0003/((1/random-1)**(1/708.0000)+708.0000) + 1250)/60


def generar_random_con_restriccion(*restricciones):
    R = generar_random()
    if R in restricciones:
        return generar_random_con_restriccion(restricciones)
    else:
        return R


### END FDPS ###

class VariablesGlobales():
    def __init__(self, N, P, TF):
        # N: Numero de operadores trbajando en el call-center
        self.N = N
        # P: Numero de personas por limite en la cola
        self.P = P
        # TF: Tiempo final.
        self.TF = TF
        # HV: High Value
        self.HV = float('inf')

        # ___________________________________
        # INITIAL CONDITIONS

        # NS: Numero de personas en el sistema
        self.NS = 0
        # NT: Numero de personas totales que ingresaron al sistema
        self.NT = 0
        #   SPVNA: Sumatoria de personas que viajan dentro de los proximos 3 dias y no son atendidas.
        self.SPVNA = 0
        # SPS: Sumatoria de permanencia en el sistema 
        self.SPS = float(0)
        #  STA: Sumatoria de tiempos de atencion 
        self.STA = 0
        #  DTAA: Diccionario de tiempos de atencion  auxiliar
        self.DTAA = {}
        # STO(i): Sumatoria de tiempo ocioso por operador
        self.STO = [0] * self.N
        # TPLL: Tiempo de llegada del llamado del cliente al call-center.
        self.TPLL = 0
        # TPS(i): Tiempo de salida del sistema del cliente por operador.
        self.TPS = [self.HV] * self.N
        # ITO(i): Comienzo de tiempo ocioso por operator
        self.ITO = [0] * self.N
        #   PPVNA = Porcentaje de personas que viajan dentro de los proximos 3 dias y no son atendidas
        self.PPVNA = 0
        # PTO(i) = Porcentaje de tiempo ocioso de cada operador 
        self.PTO = [0] * self.N
        # PTA =  Promedio de tiempo de atención de los operadores
        self.PTA = 0
        # PTE =  Promedio de tiempo de espera total de los clientes en minutos 
        self.PTE = 0
        # T = Tiempo actual
        self.T = 0


####### START FUNCIONES #########
def menor_tps(ctx):
    return ctx.TPS.index(min(ctx.TPS))


def generar_random():
    return random.uniform(0, 1)


def obtener_operador_desocupado(ctx):
    return ctx.TPS.index(ctx.HV)


###### END FUNCIONES ###########

##### START FINALIZACION #######
def imprimir_resultados(ctx):
    print("Variables de control elegidas")
    print(f"N (Numero de operadores trbajando en el call-center): {ctx.N}")
    print(f"P (Numero de personas por limite en la cola): {ctx.P}")
    print(f"TF (Tiempo final de simulacion): {ctx.TF}")
    print("___________________________")
    print("Resultados")
    print(f"Porcentaje de personas que viajan dentro de los proximos 3 dias y no son atendidas: {ctx.PPVNA}")
    for operador in range(ctx.N):
        if ctx.PTO[operador] != 0:
            print(f"Porcentaje de tiempo ocioso operador {operador}: {ctx.PTO[operador]}%")
    print("Los demas operadores tienen 0 como pocentaje de tiempo ocioso")
    print(f"Promedio de tiempo de atencion: {ctx.PTA} minutos")
    print(f"Promedio de tiempo de espera: {ctx.PTE} minutos")
    print(f"Sumatoria de tiempo de atencion: {ctx.STA} minutos")
    print(f"Sumatoria de permanencia en el sistema: {ctx.SPS} minutos")
    print(f"Auxiliar tiempos de atencion: {ctx.DTAA}")




def ir_al_final(ctx):
    if ctx.T < ctx.TF:
        # Hay que importarlo aca para evitar la referencia circular
        empezar_simulacion(ctx)
    else:
        ctx.PPVNA = ctx.SPVNA * 100 / ctx.NT
        ctx.PTA = ctx.STA / ctx.N
        ctx.PTE = (ctx.SPS - ctx.STA) / ctx.NT
        for operador in range(ctx.N):
            ctx.PTO[operador] = ctx.STO[operador] * 100 / ctx.T
        imprimir_resultados(ctx)


##### END FINALIZACION ####

#### START RAMA SALIDA ###


def asignar_proximo_tps(ctx, indice_operador):
    R = generar_random()
    if R > 0.78:
        # Atencion de reserva con un unico elemento
        tiempo_de_atencion_producto_individual = tai()
        ctx.TPS[indice_operador] = ctx.T + tiempo_de_atencion_producto_individual
        # En vez de sumar los tiempos de atencion directamente, se agregan a una variable
        # auxiliar para luego ser sumados en la salida.
        ctx.DTAA[indice_operador] = tiempo_de_atencion_producto_individual
    else:
        # Atencion de reserva con un paquete
        tiempo_de_atencion_paquete = tap()
        ctx.TPS[indice_operador] = ctx.T + tiempo_de_atencion_paquete
        # En vez de sumar los tiempos de atencion directamente, se agregan a una variable
        # auxiliar para ser sumados en la salida.
        ctx.DTAA[indice_operador] = tiempo_de_atencion_paquete


def ejecutar_rama_salida(ctx, indice_operador):
    ctx.SPS += (ctx.TPS[indice_operador] - ctx.T) * ctx.NS
    # Sumo la  el tiempo de atencion de la llegada guardado en variable auxiliar.
    # Se hace de esta manera porque debido al corto IA, al momento de imprimir los resultados
    # SPS terminaba siendo menor que STA.
    ctx.STA += ctx.DTAA[indice_operador]
    ctx.T = ctx.TPS[indice_operador]
    ctx.NS -= 1
    if ctx.NS >= ctx.N:
        # atiende operador siguiente persona
        asignar_proximo_tps(ctx, indice_operador)
    else:
        # operador queda ocioso
        ctx.TPS[indice_operador] = ctx.HV
        ctx.ITO[indice_operador] = ctx.T

    ir_al_final(ctx)


#### END RAMA SALIDA ###


##### START RAMA LLEGADA ######

def atencion_inmediata(ctx):
    operador_desocupado = obtener_operador_desocupado(ctx)
    asignar_proximo_tps(ctx, operador_desocupado)

    ctx.STO[operador_desocupado] += ctx.T - ctx.ITO[operador_desocupado]


def ejectutar_rama_llegada(ctx):
    ctx.SPS += (ctx.TPLL - ctx.T) * ctx.NS
    ctx.T = ctx.TPLL
    intervalo_de_arribo = ia()
    ctx.TPLL = ctx.T + intervalo_de_arribo
    R = generar_random()
    if R <= 0.65:
        # Persona con reserva en el intervalo de 3 dias
        ctx.NT += 1
        if ctx.NS < ctx.P:
            # Hay espacio en cola para atender la llamada
            ctx.NS += 1
            if ctx.NS <= ctx.N:
                atencion_inmediata(ctx)
        else:
            # Cantidad limite de personas superada
            ctx.SPVNA += 1

    ir_al_final(ctx)


##### END RAMA LLEGADA ######

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
    tiempo_final_de_simulacion = obtenerNumero("Ingrese tiempo final de simulacion")

    variables_globales = VariablesGlobales(cantidad_operadores, maximo_en_cola, tiempo_final_de_simulacion)
    empezar_simulacion(variables_globales)
