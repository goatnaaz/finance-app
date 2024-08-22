from telegram import Update,ReplyKeyboardMarkup
from UserTransactions import UserTr
from User import User
from Expences import Expences
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    
)


user_tr= UserTr()
user= User()
expences= Expences()

# создам кастомную клавиатуру
reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


# Курс валют по отношению к доллару
exchange_rates = {
    'usd': 1.0,  # курс доллара к доллару
    'eur': 1.1,  # курс евро к доллару (примерный)
    'grn': 0.027, # курс гривны к доллару (примерный)
    'ron': 0.22   # курс румынского лея к доллару (примерный)
}

#  Команда /start для преведствования пользователя и ознакомления с функционалом
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('''Hi! Welcome to the Finance helper telegram bot and thats what i can do:

Press /balance to see how much money you got on you right now
                                    
Press /deposit to add money to your balance in different currencies(usd,eur,ron,grn)
                                    
Press /spend to tell me if you spend money on something
                                    
Press /spendings to see all of your expences 
                                    
Use me and enjoy it ''',reply_markup=markup)

# Команда /deposit - пополнение счета
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите сумму и валюту (usd, eur, grn, ron) для пополнения:")

# Команда /spend - учет расходов
async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите сумму, валюту и причину расхода (например: '50 usd на еду'):")

# Обработчик сообщений (для пополнения счета или расходов)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_tr.set_user_id(update.message.chat_id)
    text = update.message.text.split()

    if len(text) == 2 :  # Пополнение счета
        amount_str, currency = text
        if amount_str.isdigit() and currency.lower() in exchange_rates:
            user_tr.set_user_currency(currency)
            user_tr.set_amount(float(amount_str))
            user_tr.set_actual_amount(user_tr.get_amount() * exchange_rates[currency.lower()])
            
            
            user.add(user_tr)

            await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_user_currency()} конвертировано и добавлено на ваш счет как {user_tr.get_actual_amount():.2f} USD!")
        else:
            await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron).")

    elif len(text) >= 3 :  # Учет расходов
        amount_str, currency, *reason = text
        reason = ' '.join(reason) 
        if amount_str.isdigit() and currency.lower() in exchange_rates:
            expences.set_reasons(reason)
            user_tr.set_user_currency(currency)
            user_tr.set_amount(float(amount_str))
            user_tr.set_actual_amount(user_tr.get_amount() * exchange_rates[currency.lower()])
            
            
            if user.get_total() > 0:
                expences.set_expences(user_tr.get_actual_amount())
                await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_user_currency()} ({user_tr.get_actual_amount():.2f} USD) потрачено на {reason}. Остаток на счете: {user.get_total():.2f} USD.")
            else:
                await update.message.reply_text("Недостаточно средств на счете или счет не был пополнен.")
        else:
            await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron) и причину.")

    else:
        await update.message.reply_text("Неправильный ввод. Попробуйте снова.")
    
    
    

# Команда /balance - проверка баланса
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    

    if user.get_total() > 0:
        await update.message.reply_text(f"Ваш баланс: {user.get_total()} : USD")
    else:
        await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")


#  Команда /spendings показывающая список растрат
async def spendings(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
    counter= 0
    numbers= 1
    
    if expences.get_expences_length() > 0:
        await update.message.reply_text('Here is all of your expeces')
        for i in expences.get_expences():
            await update.message.reply_text(f"{numbers}) {i} USD потрачено на {expences.get_reasons(counter)} ")
            
            numbers +=1
            counter +=1
        
    else:
        await update.message.reply_text("Пока что нет никаких растрат")


if __name__ == '__main__':
    # Создаем приложение
    application = ApplicationBuilder().token("7270199607:AAHx0yWgDxRFGtqvfSkzA3aQw7y--jVVlds").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("deposit", deposit))
    application.add_handler(CommandHandler("spend", spend))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("spendings",spendings))
    
    # Регистрируем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()
