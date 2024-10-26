#programa una simulacion de linea de espera
#una peluqueria tiene un peluquero que se demora entre 15 y 30 minutos por corte. La peluqueria recibe en promedio 3 clientes por hora (es decir, uno cada 20 minutos). Se desea simular las llegadas y servicios de los 5 clientes

import random
from re import escape
import simpy
import math
from classApp.methods.Singleton import SingletonMeta

class Peluqueria(metaclass=SingletonMeta):

  semilla: int
  num_peluqueros: int
  tiempo_corte_min: float
  tiempo_corte_max: float
  t_llegadas: float
  tot_clientes: int
  te: float #tiempo de espera total
  dt: float#duracion del servicio
  fin:float#minuto en que finaliza
  _resultText: str

  def __init__(self, semilla: int=30, num_peluqueros: int=1, tiempo_corte_min: float=15, tiempo_corte_max: float=30, t_llegadas: float=20, tot_clientes: int=5) -> None:
    self.semilla = semilla
    self.num_peluqueros = num_peluqueros
    self.tiempo_corte_min = tiempo_corte_min
    self.tiempo_corte_max = tiempo_corte_max
    self.t_llegadas = t_llegadas
    self.tot_clientes = tot_clientes
    self.te = 0
    self.dt = 0
    self.fin = 0
    self.log = []
    
    random.seed(self.semilla)
    self.env = simpy.Environment()
    self.personal = simpy.Resource(self.env, self.num_peluqueros)

  def reset(self) -> None:
      self.te = 0 
      self.dt = 0 
      self.fin = 0
      self.log = []
      random.seed(self.semilla)
      self.env = simpy.Environment()
      self.personal = simpy.Resource(self.env, self.num_peluqueros)
      
  #procedimientos
  def cortar(self, cliente) -> None:
    R = random.random()
    tiempo = self.tiempo_corte_max - self.tiempo_corte_min
    tiempo_corte = self.tiempo_corte_min + (tiempo*R) #dist Uniforme
    yield self.env.timeout(tiempo_corte) #dejar correr el tiempo n minutos
    self.log.append("Corte listo a %s en %.2f minutos" % (cliente, tiempo_corte))
    self.dt += tiempo_corte #acumular tiempo de uso de la instalacion

  def cliente(self, name) -> None:
    llega = self.env.now # guarda el minuto de llegada del cliente 
    self.log.append("--> %s llegó a la peluqueria en el minuto %.2f" % (name, llega))
    with self.personal.request() as request: # espera turno
        yield request # obtener turno
        pasa = self.env.now
        espera = pasa - llega # acumulo tiempo de espera
        self.te += espera # acumulo tiempo de espera
        self.log.append("%s Pasa y espera en la peluqueria en el minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
        yield self.env.process(self.cortar(name)) # llamar al proceso cortar
        deja = self.env.now # momento en que el cliente deja la peluquería
        self.log.append("<-- %s deja la peluqueria en minuto %.2f" % (name, deja))
        self.fin = deja # guardo el minuto en que termina


  def principal(self) -> None:
    llegada = 0
    i = 0
    for i in range(self.tot_clientes):
      R = random.random()
      llegada = -self.t_llegadas* math.log(R)
      yield self.env.timeout(llegada) #dejo transcurrir un tiempo entre un cliente y otro
      i=i+1
      self.env.process(self.cliente('cliente %d' % i))

  def result(self) -> None:
      self.reset()
      self.env.process(self.principal())
      self.env.run()
      lpc = self.te / self.fin
      tep = self.te / self.tot_clientes
      upi = (self.dt / self.fin) / self.num_peluqueros
      self._resultText = f"LPC: {lpc:.2f} \nTEP: {tep:.2f} \nUPI: {upi:.2f}"

  def set_atr(self, semilla: int, num_peluqueros: int, tiempo_corte_min: float, tiempo_corte_max: float, t_llegadas: float, tot_clientes: int):
    self.semilla = semilla
    self.num_peluqueros = num_peluqueros
    self.tiempo_corte_min = tiempo_corte_min
    self.tiempo_corte_max = tiempo_corte_max
    self.t_llegadas = t_llegadas
    self.tot_clientes = tot_clientes

  def getResultText(self) -> str: 
    return self._resultText
    
  def getLog(self) -> []:
    return self.log

if __name__ == '__main__':
    p1 = Peluqueria()
    p2 = Peluqueria()
    if id(p1) == id(p2):
        print('This Same')
    else:
        print('NOT Same')
    p1.result()
    p2.set_atr(30, 1, 15, 30, 20, 5)
    p2.result()