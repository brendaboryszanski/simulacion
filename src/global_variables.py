class VariablesGlobales():
    def __init__(self, N, P):
        # N: Numero de operadores trbajando en el call-center
        self.N = N
        # P: Numero de personas por limite en la cola
        self.P = P
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
        # STO(i): Sumatoria de tiempo ocioso por operador
        self.STO = [0] * self.N
        # TPLL: Tiempo de llegada del llamado del cliente al call-center.
        self.TPLL = 0
        # TPS(i): Tiempo de salida del sistema del cliente por operador.
        self.TPS = [self.HV] * self.N
        # TF: Tiempo final.
        self.TF = 10
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
