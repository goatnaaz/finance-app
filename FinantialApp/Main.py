from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    
)

# создам кастомную клавиатуру
reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# Создаем переменную для хранения общей суммы в долларах
user_data = {}

# переменные для хранения растрат и причин на них для команды /spendings
money_spend=[]
reasons=[]

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
    chat_id = update.message.chat_id
    text = update.message.text.split()

    if len(text) == 2 :  # Пополнение счета
        amount_str, currency = text
        if amount_str.isdigit() and currency.lower() in exchange_rates:
            amount = float(amount_str)
            amount_in_usd = amount * exchange_rates[currency.lower()]
            
            if chat_id in user_data:
                user_data[chat_id] += amount_in_usd
            else:
                user_data[chat_id] = amount_in_usd

            await update.message.reply_text(f"{amount} {currency.upper()} конвертировано и добавлено на ваш счет как {amount_in_usd:.2f} USD!")
        else:
            await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron).")

    elif len(text) >= 3 :  # Учет расходов
        amount_str, currency, *reason = text
        reason = ' '.join(reason)  # Соединяем все слова после суммы и валюты в строку
        if amount_str.isdigit() and currency.lower() in exchange_rates:
            amount = float(amount_str)
            amount_in_usd = amount * exchange_rates[currency.lower()]
            
            if chat_id in user_data and user_data[chat_id] >= amount_in_usd:
                user_data[chat_id] -= amount_in_usd
                await update.message.reply_text(f"{amount} {currency.upper()} ({amount_in_usd:.2f} USD) потрачено на {reason}. Остаток на счете: {user_data[chat_id]:.2f} USD.")
            else:
                await update.message.reply_text("Недостаточно средств на счете или счет не был пополнен.")
        else:
            await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron) и причину.")

    else:
        await update.message.reply_text("Неправильный ввод. Попробуйте снова.")
    
    context.user_data["last_command"] = None  # Сброс команды
    money_spend.append(amount_in_usd)
    reasons.append(reason)

# Команда /balance - проверка баланса
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    if chat_id in user_data:
        await update.message.reply_text(f"Ваш баланс: {user_data[chat_id]:.2f} USD")
    else:
        await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")


#  Команда /spendings показывающая список растрат
async def spendings(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
    counter= 0
    numbers= 1
    await update.message.reply_text('Here is all of your expeces')
    if len(money_spend) > 0:
        for i in money_spend:
            await update.message.reply_text(f"{numbers}) {i} USD потрачено на {reasons[counter]}")
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
