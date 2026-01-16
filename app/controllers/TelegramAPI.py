from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.models import Pokemon
import Pokedex
import random

TOKEN = '8248824617:AAFpL0RKQA2hucCgJ_CxLxS04KRxQz6F-w4'
# --- Comandos ---

async def command1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Un poco lioso pero basicamente son varios condicionales
    #Muestra el equipo que le pregunten por Telegram y diferentes mensqajes para los diferentes tipos de caso limite
    user = update.effective_user
    name = user.first_name

    nombreApp = Pokedex.getUserByTelegram(name) #Pide el nombre de APP del usuario de TG
    equipos = Pokedex.getEquipoByUser(nombreApp) #Pide los equipos del nombreAPP
    if context.args:
        k=0
        found = False
        while len(equipos)-1>=k and not found:
            if equipos[k].nombre ==context.args[0]:
                print(f"Comparing {equipos[k].nombre} and {context.args[0]}")
                found = True
            k = k + 1
        if found:
            if len(equipos[k-1].pokemons)==0:
                await update.message.reply_text(f"Tu equipo está vacío")
            else:
                for pokemon in equipos[k-1].pokemons:
                    await update.message.reply_text(f"{pokemon.nombreEspecie} nombrado: {pokemon.nombre}")

        elif not found:
            await update.message.reply_text("No encontré ese nombre de equipo en tus equipos")
    else:
        await update.message.reply_text(
            f"Hola {name}! ¿O debería llamarte {nombreApp}? Si quieres saber mas sobre un equipo, escribe su nombre como argumento. Aquí tienes tus equipos:")
        if len(equipos)>0:
            for equipo in equipos:
                await update.message.reply_text(f"{equipo.nombre} creado el {equipo.fechaCreacion}")
        else:
            await update.message.reply_text(f"[No hay equipos que mostrar...]")

async def command2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    # Piedra papel tijera pero pokemon
    if context.args:
        tipoUsuario = context.args[0]
        if tipoUsuario == "fuego" or tipoUsuario == "agua" or tipoUsuario == "planta":
            numero = random.randint(1, 3)
            resultado = 0 #Egocentrico
            if numero == 1: #Fuego
                numero = "Fuego"
                if tipoUsuario == "planta":
                    resultado = 1
                elif tipoUsuario == "agua":
                    resultado = -1
                else: resultado = 0
            elif numero == 2: #Agua
                numero = "Agua"
                if tipoUsuario == "planta":
                    resultado = -1
                elif tipoUsuario == "agua":
                    resultado = 0
                else:resultado = 1
            elif numero == 3:
                numero = "Planta"
                if tipoUsuario == "planta":
                    resultado = 0
                elif tipoUsuario == "agua":
                    resultado = 1
                else:
                    resultado = -1
            await update.message.reply_text(
                f"Elijo {numero}!!!!!")
            if resultado == 0:
                await update.message.reply_text("Es un empate!")
            elif resultado == 1:
                await update.message.reply_text("Gano yo :)")
            else:
                await update.message.reply_text("Me has ganado :(")

        else:
            await update.message.reply_text(
                f"Tu tipo no es valido! Escribe una de las tres opciones en minusculas (agua,fuego,planta)")

    else:
        await update.message.reply_text(f"Hola {name}, bienvenid@ a Agua, Fuego o Planta! La versión Pokemon de piedra papel o tijera. Si quieres jugar simplementa usa el comando de nuevo incluyendo tu tipo en minúsculas")

# --- Main ---

def main():
    print("Starting Telegram bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("command1", command1))
    app.add_handler(CommandHandler("command2", command2))

    app.run_polling()
    print("Telegram bot started")
if __name__ == "__main__":
    main()