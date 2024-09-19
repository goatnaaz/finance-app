from Commands.commands import Commands


from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    
)

class Telegram():

    _application= None

    def __init__(self,token) :
        commands= Commands()
        application = ApplicationBuilder().token(token).build()
        
    
        self._application= application

        # Регистрируем обработчики команд
        self._application.add_handler(CommandHandler("start",commands.start))
        self._application.add_handler(CommandHandler("deposit", commands.deposit))
        self._application.add_handler(CommandHandler("spend", commands.spend))
        self._application.add_handler(CommandHandler("balance", commands.balance))
        self._application.add_handler(CommandHandler("spendings",commands.spendings))
    
        # Регистрируем обработчик сообщений
        self._application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.handle_message))

    def run_application(self):
        self._application.run_polling()

    

        