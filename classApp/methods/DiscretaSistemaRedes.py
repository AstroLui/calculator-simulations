"""
Una empresa de telecomunicaciones necesita evaluar el desempeño de su servidor de red, el cual gestiona el tráfico de datos de los usuarios. Este servidor se encarga de procesar paquetes de datos que llegan de manera continua a través de la red. Debido a la capacidad limitada del servidor, solo puede atender a un número reducido de paquetes simultáneamente, y si la cola de espera para procesar más paquetes se llena, los paquetes adicionales son descartados, lo que implica una pérdida de datos.

Detalles del Sistema:
El servidor tiene una capacidad de procesamiento de un paquete a la vez.
Existe una cola de espera con un límite de 5 paquetes. Si un paquete llega y la cola ya está llena, el paquete se pierde.
Los paquetes de datos llegan al servidor de manera aleatoria, con un intervalo promedio de llegada de 3 segundos entre un paquete y otro.
El tiempo que tarda el servidor en procesar cada paquete varía entre 2 y 5 segundos.
Se desea analizar el comportamiento del servidor durante la llegada de 50 paquetes.
Objetivos de la Simulación:
Determinar el tiempo promedio de espera de los paquetes antes de ser procesados.
Calcular la tasa de pérdida de paquetes, es decir, el porcentaje de paquetes que se descartan debido a la falta de espacio en la cola.
Evaluar la utilización del servidor, para conocer qué porcentaje del tiempo está ocupado procesando paquetes versus el tiempo que está disponible.
Consideraciones Adicionales:
Se asume que la llegada de los paquetes sigue una distribución exponencial con un tiempo promedio entre llegadas de 3 segundos, lo que simula un tráfico de datos aleatorio.
Los tiempos de procesamiento de los paquetes se distribuyen de manera uniforme entre 2 y 5 segundos.
La simulación debe ejecutarse con una semilla aleatoria fija para asegurar que los resultados sean reproducibles y comparables en distintos experimentos.
Pregunta:
¿Cómo afecta la capacidad limitada de la cola y del servidor al desempeño general de la red, en términos de tiempo de espera, pérdidas de paquetes y utilización del servidor?

Contexto de Uso:
Este modelo de simulación es útil para la empresa de telecomunicaciones porque le permite:

Ajustar la capacidad del servidor y de la cola para mejorar la experiencia de los usuarios.
Identificar posibles problemas de pérdida de datos y cómo afectan la calidad del servicio.
Planificar mejoras en su infraestructura de red para reducir el tiempo de espera y optimizar el uso del servidor.
Con esta simulación, la empresa podrá tomar decisiones informadas sobre la configuración de su servidor y la capacidad de la cola para asegurar un rendimiento óptimo del sistema de red.
"""
import simpy
import random

class Redes():
    _resultText: str
    def __init__(self, semilla:int=42, cap_servidor:int=1,cap_cola:int=5,t_pros_min:int=2,
                 t_pros_max:int=5,t_llegadas:float=3,t_paquetes:int=50) -> None:
        self.SEMILLA = semilla
        self.CAPACIDAD_SERVIDOR = cap_servidor
        self.CAPACIDAD_COLA = cap_cola
        self.TIEMPO_PROCESAMIENTO_MIN = t_pros_min
        self.TIEMPO_PROCESAMIENTO_MAX = t_pros_max
        self.TIEMPO_LLEGADAS = t_llegadas
        self.TOTAL_PAQUETES = t_paquetes

        self.paquetes_perdidos = 0
        self.tiempo_total_espera = 0
        self.paquetes_procesados = 0
        self.log = []

    def reset(self) -> None:
        self.paquetes_perdidos = 0
        self.tiempo_total_espera = 0
        self.paquetes_procesados = 0
        self.log = []

    # Función para simular el proceso de un paquete
    def paquete(self, env, nombre, servidor) -> None:
        llegada = env.now  # Momento de llegada del paquete al sistema
        self.log.append(f'{nombre} llega al servidor en el segundo {llegada:.2f}')

        with servidor.request() as req:
            # Si el servidor y la cola están llenos, el paquete se pierde
            if len(servidor.queue) >= self.CAPACIDAD_COLA:
                self.paquetes_perdidos += 1
                self.log.append(
                    f'{nombre} se pierde debido a cola llena en el segundo {env.now:.2f}'
                )
                return

            # El paquete espera su turno en la cola si es necesario
            yield req
            espera = env.now - llegada
            self.tiempo_total_espera += espera
            self.log.append(
                f'{nombre} comienza a ser procesado después de esperar {espera:.2f} segundos en el segundo {env.now:.2f}'
            )

            # Simula el tiempo de procesamiento del paquete
            tiempo_procesamiento = random.randint(self.TIEMPO_PROCESAMIENTO_MIN,
                                                self.TIEMPO_PROCESAMIENTO_MAX)
            yield env.timeout(tiempo_procesamiento)
            self.log.append(f'{nombre} termina de ser procesado en el segundo {env.now:.2f}')
            self.paquetes_procesados += 1


    # Función para la llegada de paquetes
    def llegada_paquetes(self,env, servidor) -> None:
        """Genera la llegada de paquetes al servidor."""
        for i in range(self.TOTAL_PAQUETES):
            yield env.timeout(random.expovariate(
                1.0 / self.TIEMPO_LLEGADAS))  # Tiempo entre llegadas de paquetes
            env.process(self.paquete(env, f'Paquete {i+1}', servidor))

    def result(self) -> None:
        # Configuración y ejecución de la simulación
        self.reset()
        random.seed(self.SEMILLA)  # Establece la semilla para reproducir resultados
        env = simpy.Environment()  # Crea el entorno de simulación
        servidor = simpy.Resource(env, self.CAPACIDAD_SERVIDOR)  # Crea el recurso del servidor con su capacidad
        env.process(self.llegada_paquetes(env, servidor))  # Inicia el proceso de llegada de paquetes
        env.run()  # Ejecuta la simulación

        #Cálculos
        tasaDePerdida = 100 * self.paquetes_perdidos / self.TOTAL_PAQUETES if self.TOTAL_PAQUETES > 0 else 0
        tiempoPromedioEspera = self.tiempo_total_espera / self.paquetes_procesados if self.paquetes_procesados > 0 else 0
        utilizacionServidor = 100 * (self.paquetes_procesados * (self.TIEMPO_PROCESAMIENTO_MIN + self.TIEMPO_PROCESAMIENTO_MAX) / 2) / env.now if env.now > 0 else 0

        self._resultText = f"""
        Total de paquetes simulados: {self.TOTAL_PAQUETES}
        Paquetes procesados: {self.paquetes_procesados}
        Paquetes perdidos: {self.paquetes_perdidos}
        Tasa de pérdida de paquetes: {tasaDePerdida:.2f}%
        Tiempo promedio de espera de los paquetes: {tiempoPromedioEspera:.2f} segundos
        Utilización del servidor: {utilizacionServidor:.2f}%
        """
        # Salidas de la simulación
            
    def set_atr(self,semilla:int, cap_servidor:int,cap_cola:int,t_pros_min:int,
                 t_pros_max:int,t_llegadas:float,t_paquetes:int) -> None:
        self.SEMILLA = semilla
        self.CAPACIDAD_SERVIDOR = cap_servidor
        self.CAPACIDAD_COLA = cap_cola
        self.TIEMPO_PROCESAMIENTO_MIN = t_pros_min
        self.TIEMPO_PROCESAMIENTO_MAX = t_pros_max
        self.TIEMPO_LLEGADAS = t_llegadas
        self.TOTAL_PAQUETES = t_paquetes

    def getResultText(self) -> None:
        return self._resultText
    
    def getLog(self) -> None:
        return self.log