import simpy
import random
from classApp.methods.Singleton import SingletonMeta
class Restaurante2(metaclass=SingletonMeta):
    # Parámetros de la simulación
    SEMILLA: int  # Semilla para reproducibilidad
    NUM_MESAS:int  # Número de mesas disponibles en el restaurante
    TIEMPO_COMER_MIN:int # Tiempo mínimo que un cliente pasa comiendo (minutos)
    TIEMPO_COMER_MAX:int  # Tiempo máximo que un cliente pasa comiendo (minutos)
    TIEMPO_LLEGADAS:int  # Tiempo promedio entre la llegada de clientes (minutos)
    TOTAL_CLIENTES:int# Total de clientes a simular

    def __init__(self, semilla: int=42, num_mesas: int=5, tiempo_comer_min:int=20, tiempo_comer_max:int=40, tiempo_llegadas:int=10, total_clientes:int=10):
        self.SEMILLA = semilla
        self.NUM_MESAS = num_mesas
        self.TIEMPO_COMER_MIN = tiempo_comer_min
        self.TIEMPO_COMER_MAX = tiempo_comer_max
        self.TIEMPO_LLEGADAS = tiempo_llegadas
        self.TOTAL_CLIENTES = total_clientes
        self.log = []

    # Función para simular el proceso de un cliente
    def cliente(self, env, nombre, restaurante):
        """Simula el proceso de un cliente que llega, espera una mesa, come y luego se va."""
        self.log.append(f'{nombre} llega al restaurante en el minuto {env.now:.2f}')

        # El cliente solicita una mesa en el restaurante (espera si no hay mesas disponibles)
        with restaurante.request() as mesa:
            yield mesa  # Espera a que una mesa esté disponible
            self.log.append(f'{nombre} toma una mesa en el minuto {env.now:.2f}')

            # Simula el tiempo que el cliente pasa comiendo
            tiempo_comer = random.randint(self.TIEMPO_COMER_MIN, self.TIEMPO_COMER_MAX)
            yield env.timeout(tiempo_comer)
            self.log.append(
                f'{nombre} termina de comer y deja la mesa en el minuto {env.now:.2f}'
            )


    # Función para la llegada de clientes
    def llegada_clientes(self, env, restaurante):
        """Genera la llegada de clientes al restaurante."""
        for i in range(self.TOTAL_CLIENTES):
            # Cada cliente llega al restaurante
            yield env.timeout(
                random.expovariate(1.0 / self.TIEMPO_LLEGADAS)
            )  # Distribución exponencial para el tiempo entre llegadas
            env.process(self.cliente(env, f'Cliente {i+1}', restaurante))

    def result(self):
        self.log = []
        # Configuración y ejecución de la simulación
        random.seed(self.SEMILLA)  # Establece la semilla para reproducir resultados
        env = simpy.Environment()  # Crea el entorno de simulación
        restaurante = simpy.Resource(
            env, self.NUM_MESAS)  # Crea el recurso de mesas en el restaurante
        env.process(self.llegada_clientes(
            env, restaurante))  # Inicia el proceso de llegada de clientes
        env.run()  # Ejecuta la simulación

        return self.log
    
    def set_atr(self,semilla: int, num_mesas: int, tiempo_comer_min:int, tiempo_comer_max:int, tiempo_llegadas:int, total_clientes:int):
        self.SEMILLA = semilla
        self.NUM_MESAS = num_mesas
        self.TIEMPO_COMER_MIN = tiempo_comer_min
        self.TIEMPO_COMER_MAX = tiempo_comer_max
        self.TIEMPO_LLEGADAS = tiempo_llegadas
        self.TOTAL_CLIENTES = total_clientes
