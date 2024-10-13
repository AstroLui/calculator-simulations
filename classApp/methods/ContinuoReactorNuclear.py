import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from classApp.methods.Singleton import SingletonMeta

class Nuclear(metaclass=SingletonMeta):
    # Atributo de la clase
    _Q_gen: float # Tasa de generacion de calor en vatios (W)
    _K: float # Coeficiente de enfriamiento en W/C
    _T_cool: float # Temperatura del sistema de enfriamiento en grados Celsius
    _C: float # Capaciadad termica del reactor 
    _T0: float # Temperatura inicial del reactro
    _tiempo = np.linspace(0, 200, 1000)  # Tiempo en minutos

    # Para instanciar la clase
    def __init__(self, Q_get:float=5000, K:float=0.1, T_cool:float=25, C:float=10000, T0:float=150) -> None: 
        self._Q_gen = Q_get
        self._K = K
        self._T_cool = T_cool
        self._C = C
        self._T0 = T0
    
    # Ecuacion diferencial para la variacion de la temperatura
    def modelo(self, T, t) -> float:
        self.dT_dt = (self._Q_gen / self._C) - self._K * (T - self._T_cool)
        return self.dT_dt     

    # Resolver la ecuacion diferencia y 
    # Mostrar la grafica de los resultados
    def resutl(self) -> None:
        solucion = odeint(self.modelo, self._T0, self._tiempo)
        plt.figure(figsize=(10, 5))
        plt.plot(self._tiempo, solucion, label='Temperatura del Reactor')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Enfriamiento del Reactor Nuclear')
        plt.axhline(self._T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
        plt.grid(True)
        plt.legend()
        plt.show()

    # Setter de los atributos
    def set_atr(self, Q_gen:float, K:float, T_cool:float, C:float, T0:float=150) -> None:
        self._Q_gen = Q_gen
        self._K = K
        self._T_cool = T_cool
        self._C = C
        self._T0 = T0

if __name__ == "__main__":
    n1 = Nuclear()
    n2 = Nuclear()
    if id(n1) == id(n2): 
        print('BRUH its the SAME')
    else:
        print('NOT Same')
    n1.resutl()
    n2.set_atr(6000,0.5,40,20000, 200)
    n2.resutl()