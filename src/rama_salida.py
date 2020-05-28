from src.fdps import *
from src.functions import *
from src.parte_final import *

def asignar_proximo_tps(ctx, indice_operador):
    R = generar_random()
    if R > 0.78:
        #Atencion de reserva con un unico elemento
        tiempo_de_atencion_producto_individual = tai()
        ctx.TPS[indice_operador] = ctx.T + tiempo_de_atencion_producto_individual
        ctx.STA += tiempo_de_atencion_producto_individual
    else:
        #Atencion de reserva con un paquete
        tiempo_de_atencion_paquete = tap()
        ctx.TPS[indice_operador] = ctx.T + tiempo_de_atencion_paquete
        ctx.STA += tiempo_de_atencion_paquete


def ejecutar_rama_salida(ctx, indice_operador):
    ctx.SPS += (ctx.TPS[indice_operador] - ctx.T) * ctx.NS
    ctx.T = ctx.TPS[indice_operador]
    ctx.NS -= 1
    if ctx.NS >= ctx.N:
        #atiende operador siguiente persona
        asignar_proximo_tps(ctx, indice_operador)
    else:
        #operador queda ocioso
        ctx.TPS[indice_operador] = ctx.HV
        ctx.ITO[indice_operador] = ctx.T

    ir_al_final(ctx)
