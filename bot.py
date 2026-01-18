import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.environ.get('TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        '¡Hola! Soy PlacasMex_bot. '
        'Envía una placa mexicana (ej: ABC123) para buscar información.\n'
        'Usa /help para comandos.'
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Comandos:\n'
        '/start - Iniciar\n'
        '/help - Ayuda\n'
        'Envía una placa como "ABC123" para buscar.'
    )

async def handle_plate(update: Update, context: CallbackContext):
    plate_text = update.message.text.strip().upper()
    if len(plate_text) >= 5 and plate_text.isalnum():
        reply = f'🔍 Buscando info para: {plate_text}\n(Ejemplo. Agrega base de datos después.)'
    else:
        reply = 'Formato no válido. Ejemplo: ABC123'
    await update.message.reply_text(reply)

def main():
    if not TOKEN:
        logging.error("❌ No hay token. Configura TOKEN en Render.")
        return
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_plate))
    
    logging.info("🤖 Bot iniciado...")
    app.run_polling()

if __name__ == '__main__':
    main()
