#Controlador
from app.repositories import GestorUsuario
from app.repositories import GestorEquipo

def vincularUsuario(username):
    GestorUsuario.vincularUsuario(username)

def getUserByTelegram(TelegramUsername):
    nombreApp = GestorUsuario.buscarUsuario(TelegramUsername)
    return nombreApp
def getEquipoByUser(username):
    equipos = GestorEquipo.get_by_user(username)
    return equipos

def registrarse(username, email, password, confirm_password):
    return GestorUsuario.crearCuenta(username, email, password, confirm_password)

def iniciarSesion(username, password):
    return GestorUsuario.validarUsuario(username, password)

def actualizarDatos(username, email=None, foto=None, password=None, confirm_password=None):
    return GestorUsuario.actualizarDatos(username, email, foto, password, confirm_password)

def aprobarCuenta(username):
    return GestorUsuario.aprobarCuenta(username)

def borrarCuenta(username):
    return GestorUsuario.borrarCuenta(username)

def modificarCuenta(username, esAdmin=None, aprobado=None):
    return GestorUsuario.modificarCuenta(username, esAdmin, aprobado)

def obtenerTodosUsuarios():
    return GestorUsuario.obtenerTodosUsuarios()

def obtenerCuentasPendientes():
    return GestorUsuario.obtenerCuentasPendientes()

def obtenerCuentasAprobadas():
    return GestorUsuario.obtenerCuentasAprobadas()

def buscarPorUsername(username):
    return GestorUsuario.buscarPorUsername(username)

def seguir(seguidor, seguido):
    return GestorUsuario.seguir(seguidor, seguido)

def dejarDeSeguir(seguidor, seguido):
    return GestorUsuario.dejarDeSeguir(seguidor, seguido)

def get_following(username):
    return GestorUsuario.get_following(username)

def get_followers(username):
    return GestorUsuario.get_followers(username)