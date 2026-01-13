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