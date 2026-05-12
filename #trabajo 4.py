# =====================================================
# TRABAJO FASE 4
# SISTEMA INTEGRAL SOFTWARE FJ
# =====================================================

# Importación de librerías necesarias
from abc import ABC, abstractmethod
from datetime import datetime


# =====================================================
# FUNCIÓN PARA REGISTRO DE LOGS
# =====================================================

# Esta función guarda eventos y errores en un archivo txt
def guardar_log(mensaje):
    try:
        with open("logs.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{datetime.now()} - {mensaje}\n")

    except Exception as e:
        print("Error guardando log")
        print(e)


# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

# Excepción general del sistema
class ErrorSistema(Exception):
    pass


# Excepción específica para clientes
class ErrorCliente(ErrorSistema):
    pass


# Excepción específica para reservas
class ErrorReserva(ErrorSistema):
    pass


# =====================================================
# CLASE ABSTRACTA GENERAL
# =====================================================

# Clase base abstracta
class Entidad(ABC):

    # Constructor
    def __init__(self, id):
        self.id = id

    # Método abstracto
    @abstractmethod
    def mostrar(self):
        pass


# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Entidad):

    # Constructor del cliente
    def __init__(self, id, nombre, documento):

        # Constructor padre
        super().__init__(id)

        # Validación del nombre
        if nombre.strip() == "":
            raise ErrorCliente("El nombre del cliente está vacío")

        # Validación del documento
        if not documento.isdigit():
            raise ErrorCliente("El documento debe contener solo números")

        # Encapsulación
        self.__nombre = nombre
        self.__documento = documento

    # Mostrar información
    def mostrar(self):
        return f"Cliente: {self.__nombre} - Documento: {self.__documento}"

    # Getter nombre
    def get_nombre(self):
        return self.__nombre

    # Getter documento
    def get_documento(self):
        return self.__documento


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    # Constructor
    # [APORTE NICOLAS]: Definición del constructor de la clase abstracta Servicio. 
    # Se implementa una validación estricta de parámetros para asegurar que ningún 
    # servicio se cree con costos inconsistentes, garantizando la estabilidad 
    # del sistema Software FJ ante datos inválidos.
    def __init__(self, nombre, precio):

        # Validación del precio
        if precio <= 0:
            raise ErrorSistema("El precio debe ser mayor a cero")

        self.nombre = nombre
        self.precio = precio

    # Método abstracto
    @abstractmethod
    # [APORTE NICOLAS]: Definición de métodos abstractos para garantizar el polimorfismo. 
    # Esto obliga a que cada servicio (Sala, Equipo, Asesoría) implemente su propia 
    # lógica de costos y descripción, cumpliendo con la arquitectura modular 
    # exigida en el Anexo 3.
    def calcular_costo(self):
        pass

    # Método abstracto
    @abstractmethod
    def descripcion(self):
        pass


# =====================================================
# SERVICIO RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    # Constructor
    def __init__(self, horas):
        super().__init__("Reserva Sala", 50000)
        self.horas = horas

    # Método sobrescrito
    def calcular_costo(self, descuento=0):

        # Validación
        if self.horas <= 0:
            raise ErrorSistema("Las horas deben ser mayores a cero")

        total = self.precio * self.horas

        # Aplicación descuento
        return total - (total * descuento)

    # Descripción del servicio
    def descripcion(self):
        return f"Reserva de sala por {self.horas} horas"


# =====================================================
# SERVICIO ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    # Constructor
    def __init__(self, dias):
        super().__init__("Alquiler Equipo", 30000)
        self.dias = dias

    # Método sobrescrito
    def calcular_costo(self, impuesto=0.19):

        # Validación
        if self.dias <= 0:
            raise ErrorSistema("Los días deben ser mayores a cero")

        total = self.precio * self.dias

        # Aplicación impuesto
        return total + (total * impuesto)

    # Descripción
    def descripcion(self):
        return f"Alquiler de equipo por {self.dias} días"


# =====================================================
# SERVICIO DE ASESORÍAS
# =====================================================

class Asesoria(Servicio):

    # Constructor
    def __init__(self, tipo):
        super().__init__("Asesoría", 80000)
        self.tipo = tipo.lower()

    # Método sobrescrito
    def calcular_costo(self, horas=1):

        # Validación
        if horas <= 0:
            raise ErrorSistema("Las horas deben ser válidas")

        # Asesoría avanzada
        if self.tipo == "avanzada":
            return self.precio * horas * 1.5

        # Asesoría básica
        elif self.tipo == "basica":
            return self.precio * horas

        # Tipo inválido
        else:
            raise ErrorSistema("Tipo de asesoría inválido")

    # Descripción
    def descripcion(self):
        return f"Asesoría tipo {self.tipo}"


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    # Constructor
    def __init__(self, cliente, servicio, duracion):

        # Validación cliente
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente inválido")

        # Validación servicio
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio inválido")

        # Validación duración
        if duracion <= 0:
            raise ErrorReserva("Duración inválida")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"

    # Confirmar reserva
    def confirmar(self):

        # Validación estado
        if self.estado != "pendiente":
            raise ErrorReserva("La reserva no se puede confirmar")

        self.estado = "confirmada"

        guardar_log(f"Reserva confirmada para {self.cliente.get_nombre()}")

    # Cancelar reserva
    def cancelar(self):

        # Validación estado
        if self.estado == "cancelada":
            raise ErrorReserva("La reserva ya estaba cancelada")

        self.estado = "cancelada"

        guardar_log(f"Reserva cancelada para {self.cliente.get_nombre()}")

    # Realizar pago
    def pagar(self):

        # Validación
        if self.estado != "confirmada":
            raise ErrorReserva("Debe confirmar la reserva antes de pagar")

        total = self.servicio.calcular_costo()

        guardar_log(f"Pago realizado por valor de {total}")

        return total

    # Mostrar información
    def __str__(self):
        return f"{self.cliente.get_nombre()} - {self.servicio.descripcion()} - Estado: {self.estado}"


# =====================================================
# CLASE PRINCIPAL DEL SISTEMA
# =====================================================

class SistemaFJ:
# [APORTE NICOLÁS]: Implementación del flujo principal de registro. 
    # Se usa 'except' para capturar errores específicos, 'else' para confirmar 
    # el éxito de la operación y 'finally' para asegurar el registro en el log 
    # de eventos, manteniendo la aplicación estable en todo momento.
    
    # Constructor
    def __init__(self):

        # Listas internas
        self.clientes = []
        self.reservas = []

    # Agregar clientes
    def agregar_cliente(self, id, nombre, documento):

        try:
            cliente = Cliente(id, nombre, documento)

        # Encadenamiento de excepciones
        except ErrorCliente as e:
            guardar_log(f"Error creando cliente: {e}")
            raise ErrorSistema("Fallo en el registro del cliente") from e

        # Else obligatorio
        else:
            self.clientes.append(cliente)
            guardar_log(f"Cliente agregado correctamente: {nombre}")
            return cliente

        # Finally obligatorio
        finally:
            guardar_log("Proceso de registro de cliente finalizado")

    # Crear reserva
    def crear_reserva(self, cliente, servicio, duracion):

        try:
            reserva = Reserva(cliente, servicio, duracion)

        except ErrorReserva as e:
            guardar_log(f"Error creando reserva: {e}")
            print("No fue posible crear la reserva")

        else:
            self.reservas.append(reserva)
            guardar_log("Reserva creada exitosamente")
            return reserva

        finally:
            guardar_log("Proceso de reserva finalizado")

    # Ver reservas
    def ver_reservas(self):

        # Validación
        if len(self.reservas) == 0:
            print("No existen reservas registradas")

        else:
            for reserva in self.reservas:
                print(reserva)


# =====================================================
# SIMULACIÓN DEL SISTEMA
# =====================================================

if __name__ == "__main__":

    print("\n========== INICIO DEL SISTEMA ==========\n")

    # Crear sistema
    sistema = SistemaFJ()

    # =====================================================
    # OPERACIÓN 1 - CLIENTE VÁLIDO
    # =====================================================

    try:
        c1 = sistema.agregar_cliente(1, "Felipe", "12345")
        print("Cliente registrado correctamente")

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # OPERACIÓN 2 - CLIENTE INVÁLIDO
    # =====================================================

    try:
        sistema.agregar_cliente(2, "", "999")

    except ErrorSistema as e:
        print("Error:", e)

    # =====================================================
    # OPERACIÓN 3 - DOCUMENTO INVÁLIDO
    # =====================================================

    try:
        sistema.agregar_cliente(3, "Juan", "ABC")

    except ErrorSistema as e:
        print("Error:", e)

    # =====================================================
    # OPERACIÓN 4 - SERVICIO VÁLIDO
    # =====================================================

    try:
        sala = ReservaSala(2)
        print("Servicio de sala creado")

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # OPERACIÓN 5 - SERVICIO INVÁLIDO
    # =====================================================

    try:
        sala_error = ReservaSala(-2)
        sala_error.calcular_costo()

    except ErrorSistema as e:
        guardar_log(e)
        print("Error creando servicio")

    # =====================================================
    # OPERACIÓN 6 - ALQUILER DE EQUIPO
    # =====================================================

    try:
        equipo = AlquilerEquipo(3)
        print("Servicio de alquiler creado")

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # OPERACIÓN 7 - RESERVA EXITOSA
    # =====================================================

    try:
        r1 = sistema.crear_reserva(c1, sala, 2)

        if r1:
            r1.confirmar()
            print("Pago realizado:", r1.pagar())

    except ErrorSistema as e:
        print(e)

    else:
        print("Reserva procesada correctamente")

    finally:
        print("Fin del proceso de reserva")

    # =====================================================
    # OPERACIÓN 8 - CLIENTE INVÁLIDO EN RESERVA
    # =====================================================

    try:
        sistema.crear_reserva("cliente falso", sala, 2)

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # OPERACIÓN 9 - PAGO SIN CONFIRMAR
    # =====================================================

    try:
        r2 = sistema.crear_reserva(c1, equipo, 3)

        if r2:
            r2.pagar()

    except ErrorSistema as e:
        print("Error en pago:", e)

    # =====================================================
    # OPERACIÓN 10 - CANCELACIÓN
    # =====================================================

    try:
        if r2:
            r2.cancelar()
            print("Reserva cancelada")

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # OPERACIÓN 11 - CANCELACIÓN REPETIDA
    # =====================================================

    try:
        if r2:
            r2.cancelar()

    except ErrorSistema as e:
        print("Error:", e)

    # =====================================================
    # OPERACIÓN 12 - ASESORÍA INVÁLIDA
    # =====================================================

    try:
        asesoria = Asesoria("pro")
        asesoria.calcular_costo()

    except ErrorSistema as e:
        print("Error asesoría:", e)

    # =====================================================
    # OPERACIÓN 13 - ASESORÍA VÁLIDA
    # =====================================================

    try:
        asesoria2 = Asesoria("basica")
        total = asesoria2.calcular_costo(3)

        print("Costo asesoría:", total)

    except ErrorSistema as e:
        print(e)

    # =====================================================
    # VISUALIZACIÓN FINAL
    # =====================================================

    print("\n========== RESERVAS REGISTRADAS ==========\n")

    sistema.ver_reservas()

    print("\n========== FIN DEL SISTEMA ==========")
    print("El sistema continúa funcionando correctamente") 
