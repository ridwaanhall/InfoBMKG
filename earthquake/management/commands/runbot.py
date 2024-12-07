from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from earthquake.views import start, unsubscribe, help, handle_message
from django.conf import settings

BOT_TOKEN = settings.BOT_TOKEN

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("unsubscribe", unsubscribe))
        application.add_handler(CommandHandler("help", help))
        application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

        application.run_polling()
