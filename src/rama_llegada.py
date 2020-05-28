from src.fdps import *
from src.functions import *
from src.parte_final import *
from src.rama_salida import *

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
        #Persona con reserva en el intervalo de 3 dias
        ctx.NT += 1
        if ctx.NS < ctx.P:
            #Hay espacio en cola para atender la llamada
            ctx.NS += 1
            if ctx.NS <= ctx.N:
                atencion_inmediata(ctx)
        else:
            #Cantidad limite de personas superada
            ctx.SPVNA = ctx.SPVNA + 1

    ir_al_final(ctx)



