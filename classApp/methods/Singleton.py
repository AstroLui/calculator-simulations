# Patrones de Diseños
# <-- Singleton --> 
class SingletonMeta(type):
    """
        La clase Singleton es usada para asegurar que una clase
        se instancia una unica vez. Se hace asi para no dejar que 
        se instancie varias veces la misma clase si no es necesario
        siendo algo mas eficiente.
    """
    _instances = {}
    # El 'cls' es un metodo que se vincula a la clase mas no a la instancia
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

"""
    Para implementar esto a la clase que deseas, solo tienes que pasar 
    como parametro a al clase que quieras implementar esto lo siguiente:
    <-- metaclass=SingletonMeta -->
"""