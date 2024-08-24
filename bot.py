"""
Bot de Recuperación de Cuentas de Facebook

Creado por: codigo

Dependencias:
    - python-telegram-bot
    - python-dotenv

Instalar dependencias: pip install python-telegram-bot python-dotenv
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración
BOT_NAME = 'facebook_recovery_bot'
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Crear teclado inline
    keyboard = [
        [InlineKeyboardButton("Recuperar Cuenta", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Mensaje de bienvenida
    mensaje = (
        "Bienvenido al Bot de Recuperación de Cuentas de Facebook!\n\n"
        "¿Problemas para acceder? Estamos aquí para ayudarte.\n"
        "Haz clic en 'Recuperar Cuenta' para comenzar.\n"
        "Si necesitas más información, pulsa 'Ayuda'."
    )
    await update.message.reply_text(mensaje, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Texto de ayuda
    help_text = (
        "Para recuperar tu cuenta:\n"
        "1. Haz clic en 'Recuperar Cuenta'\n"
        "2. Sigue las instrucciones en la web\n"
        "3. Verifica tu identidad\n"
        "4. Crea una nueva contraseña\n\n"
        "Para más ayuda, contacta soporte de Facebook."
    )
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(help_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Manejar errores
    logger.error(f"Error: {context.error} causado por {update}")

def main():
    # Iniciar y configurar el bot
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(help_command, pattern='^help$'))
    application.add_error_handler(error_handler)
    
    # Iniciar el bot
    application.run_polling()
    logger.info("Bot iniciado correctamente")

if __name__ == '__main__':
    main()
