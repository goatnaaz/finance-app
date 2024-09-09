
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


def main():
    commands= Commands()
    
    # Создаем приложение
    application = ApplicationBuilder().token("7270199607:AAHx0yWgDxRFGtqvfSkzA3aQw7y--jVVlds").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start",commands.start))
    application.add_handler(CommandHandler("deposit", commands.deposit))
    application.add_handler(CommandHandler("spend", commands.spend))
    application.add_handler(CommandHandler("balance", commands.balance))
    application.add_handler(CommandHandler("spendings",commands.spendings))
    
    # Регистрируем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.handle_message))


     # Запускаем бота
    application.run_polling()

    

if __name__ == '__main__':

    main()
