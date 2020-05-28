

def imprimir_resultados(ctx):
    print("Variables de control elegidas")
    print(f"N (Numero de operadores trbajando en el call-center): {ctx.N}")
    print(f"P (Numero de personas por limite en la cola): {ctx.P}")
    print("___________________________")
    print("Resultados")
    print(f"Porcentaje de personas que viajan dentro de los proximos 3 dias y no son atendidas: {ctx.PPVNA}")
    for operador in range(ctx.N):
        print(f"Porcentaje de tiempo ocioso operador {operador}: {ctx.PTO[operador]}%")
    print(f"Porcentaje de tiempo de atencion: {ctx.PTA}")
    print(f"Porcentaje de tiempo de espera: {ctx.PTE}")


def ir_al_final(ctx):
    if ctx.T < ctx.TF:
        #Hay que importarlo aca para evitar la referencia circular
        from src import empezar_simulacion
        empezar_simulacion(ctx)
    else:
        ctx.PPVNA = ctx.SPVNA * 100 / ctx.NT
        ctx.PTA = ctx.STA / ctx.N
        ctx.PTE = (ctx.SPS - ctx.STA) / ctx.NT
        for operador in range(ctx.N):
            ctx.PTO[operador] = ctx.STO[operador] * 100 / ctx.T
        imprimir_resultados(ctx)



