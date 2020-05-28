
import random


def menor_tps(ctx):
    return ctx.TPS.index(min(ctx.TPS))


def generar_random():
    return random.uniform(0, 1)

def obtener_operador_desocupado(ctx):
    return ctx.TPS.index(ctx.HV)
