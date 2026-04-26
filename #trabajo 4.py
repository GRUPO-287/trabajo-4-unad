#trabajo 4
from abc import ABC, abstractmethod
from datetime import datetime

# -------------------------
# LOGS
# -------------------------
def guardar_log(mensaje):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")


# -------------------------
# EXCEPCIONES
# -------------------------
class ErrorSistema(Exception):
    pass


# -------------------------
# CLASE ABSTRACTA GENERAL
# -------------------------
class Entidad(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def mostrar(self):
        pass


# -------------------------
# CLIENTE
# -------------------------
class Cliente(Entidad):
    def __init__(self, id, nombre, documento):
        super().__init__(id)

        if nombre == "":
            raise ErrorSistema("Nombre vacío")

        if not documento.isdigit():
            raise ErrorSistema("Documento inválido")

        self.__nombre = nombre
        self.__documento = documento

    def mostrar(self):
        return f"{self.__nombre} - {self.__documento}"

    def get_nombre(self):
        return self.__nombre


# -------------------------
# SERVICIO ABSTRACTO
# -------------------------
class Servicio(ABC):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# -------------------------
# TIPOS DE SERVICIO
# -------------------------
class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Sala", 50000)
        self.horas = horas

    def calcular_costo(self, descuento=0):
        if self.horas <= 0:
            raise ErrorSistema("Horas inválidas")

        total = self.precio * self.horas
        return total - (total * descuento)

    def descripcion(self):
        return f"Sala por {self.horas} horas"


class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Equipo", 30000)
        self.dias = dias

    def calcular_costo(self, impuesto=0.19):
        if self.dias <= 0:
            raise ErrorSistema("Días inválidos")

        total = self.precio * self.dias
        return total + (total * impuesto)

    def descripcion(self):
        return f"Equipo por {self.dias} días"


class Asesoria(Servicio):
    def __init__(self, tipo):
        super().__init__("Asesoría", 80000)
        self.tipo = tipo

    def calcular_costo(self, horas=1):
        if horas <= 0:
            raise ErrorSistema("Horas inválidas")

        if self.tipo == "avanzada":
            return self.precio * horas * 1.5
        elif self.tipo == "basica":
            return self.precio * horas
        else:
            raise ErrorSistema("Tipo inválido")

    def descripcion(self):
        return f"Asesoría {self.tipo}"


# -------------------------
# RESERVA
# -------------------------
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorSistema("Cliente inválido")

        if not isinstance(servicio, Servicio):
            raise ErrorSistema("Servicio inválido")

        if duracion <= 0:
            raise ErrorSistema("Duración inválida")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"

    def confirmar(self):
        if self.estado != "pendiente":
            raise ErrorSistema("No se puede confirmar")

        self.estado = "confirmada"
        guardar_log("Reserva confirmada")

    def cancelar(self):
        if self.estado == "cancelada":
            raise ErrorSistema("Ya estaba cancelada")

        self.estado = "cancelada"
        guardar_log("Reserva cancelada")

    def pagar(self):
        if self.estado != "confirmada":
            raise ErrorSistema("Primero confirme la reserva")

        total = self.servicio.calcular_costo()
        guardar_log(f"Pago realizado: {total}")
        return total

    def __str__(self):
        return f"{self.cliente.get_nombre()} - {self.servicio.descripcion()} ({self.estado})"


# -------------------------
# SISTEMA
# -------------------------
class SistemaFJ:
    def __init__(self):
        self.clientes = []
        self.reservas = []

    def agregar_cliente(self, id, nombre, documento):
        try:
            c = Cliente(id, nombre, documento)
            self.clientes.append(c)
            return c
        except Exception as e:
            guardar_log(e)
            print("Error creando cliente")

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            r = Reserva(cliente, servicio, duracion)
            self.reservas.append(r)
            return r
        except Exception as e:
            guardar_log(e)
            print("Error creando reserva")

    def ver_reservas(self):
        for r in self.reservas:
            print(r)


# -------------------------
# SIMULACIÓN (LO IMPORTANTE)
# -------------------------
if __name__ == "__main__":

    sistema = SistemaFJ()

    print("INICIO\n")

    # 1
    c1 = sistema.agregar_cliente(1, "Felipe", "123")

    # 2 error
    sistema.agregar_cliente(2, "", "999")

    # 3 error
    sistema.agregar_cliente(3, "Juan", "ABC")

    # 4
    s1 = ReservaSala(2)

    # 5 error
    try:
        s_error = ReservaSala(-2)
        s_error.calcular_costo()
    except:
        print("Error en servicio")

    # 6
    s2 = AlquilerEquipo(3)

    # 7 reserva buena
    r1 = sistema.crear_reserva(c1, s1, 2)
    try:
        r1.confirmar()
        print("Pago:", r1.pagar())
    except:
        print("Error en reserva")

    # 8 error cliente
    sistema.crear_reserva("falso", s1, 2)

    # 9 error pago sin confirmar
    r2 = sistema.crear_reserva(c1, s2, 3)
    try:
        r2.pagar()
    except:
        print("Error: no confirmó")

    # 10 cancelar
    try:
        r2.cancelar()
    except:
        print("Error cancelando")

    # 11 cancelar otra vez
    try:
        r2.cancelar()
    except:
        print("Ya estaba cancelada")

    # 12 asesoría mala
    try:
        s3 = Asesoria("pro")
        s3.calcular_costo()
    except:
        print("Error asesoría")

    print("\nReservas:")
    sistema.ver_reservas()

    print("\nFIN - el sistema sigue funcionando")