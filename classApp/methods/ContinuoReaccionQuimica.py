import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from Singleton import SingletonMeta

class Quimica(metaclass=SingletonMeta): 
    # Atributos de la clase
    _k: float  # Constante de Velocidad de la reaccion (1/min)
    _A0: float # Concentracion inicial de A (mol/L)
    _tiempo = np.linspace(0, 50, 1000) # Tiempo de simulacion (0 a 50 min, con 1000 puntos)

    # Para Instanciar la clase
    def __init__(self, k: float=0.1, A0: float=0.1) -> None:
        self._k = k
        self._A0 = A0

    # Ecuacion diferencial para la concentracion de A
    def modelo(self, A, t) -> float:
        self.dA_dt = -self._k * A
        return self.dA_dt

    # Resolver la ecuacion diferencial y 
    # Mostrar la Grafica de los Resultados
    def result(self) -> None:
        solucion = odeint(self.modelo, self._A0, self._tiempo)
        plt.figure(figsize=(10, 5))
        plt.plot(self._tiempo, solucion, label='Concentración de [A]')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Concentración (mol/L)')
        plt.title('Descomposición de un Reactivo de Primer Orden')
        plt.grid(True)
        plt.legend()
        plt.show()

    # Setter para los atributos k y A0
    def set_atr(self, k, A0) -> None:
        self._k = k
        self._A0 = A0 
  
if __name__ == '__main__':
    q1 = Quimica()
    q2 = Quimica()
    if id(q1) == id(q2):
        print('This Same')
    else:
        print('NOT Same')
    q1.result()
    q2.set_atr(0.5, 1)
    q2.result()