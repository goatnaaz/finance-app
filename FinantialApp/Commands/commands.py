
from Entities.UserTransactions import UserTr
from Entities.User import User
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from Commands.TransactionHandler import TransactionHandler



#класс комманд для телеграм бота
class Commands():

    user_tr= object()
    user= object()

    reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
 
    
    #  Команда /start для преведствования пользователя и ознакомления с функционалом
    async def start(self,update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:

        self.user_tr= UserTr()
        self.user= User()

        self.user.set_chat_id(update.message.chat_id)

        await update.message.reply_text('''Hi! Welcome to the Finance helper telegram bot and thats what i can do:

    Press /balance to see how much money you got on you right now
                                        
    Press /deposit to add money to your balance in different currencies(usd,eur,ron,grn)
                                        
    Press /spend to tell me if you spend money on something
                                        
    Press /spendings to see all of your expences 
                                        
    Use me and enjoy it ''',reply_markup=self.markup)

    # Команда /deposit - пополнение счета
    async def deposit(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Введите сумму и валюту (usd, eur, grn, ron) для пополнения:")

    # Команда /spend - учет расходов
    async def spend(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Введите сумму, валюту и причину расхода (например: '50 usd на еду'):")

    # Обработчик сообщений (для пополнения счета или расходов)
    async def handle_message(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text.split()

        if len(text) == TransactionHandler.DEPOSIT.value:  # Пополнение счета

            amount_str, currency = text

            if amount_str.isdigit() and currency.lower() in self.user_tr.get_exchange():

                self.user_tr.create_actual_amount(currency,float(amount_str))
                self.user.add(self.user_tr)

                await update.message.reply_text(f"{self.user_tr.get_amount()} {self.user_tr.get_currency()} конвертировано и добавлено на ваш счет как {self.user_tr.get_actual_amount():.2f} USD!")
            else:
                await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron).")

        elif len(text) >= TransactionHandler.SPEND.value :  # Учет расходов

            amount_str, currency, *reason = text
            reason = ' '.join(reason) 

            if amount_str.isdigit() and currency.lower() in self.user_tr.get_exchange():

                if self.user.get_total() > 0:
                    
                    self.user_tr.create_actual_amount(currency,float(amount_str))
                    self.user_tr.set_reason(reason)
                    self.user_tr.set_expence(self.user_tr.get_actual_amount())
                
                    self.user.subtract(self.user_tr)
                    
                    await update.message.reply_text(f"{self.user_tr.get_amount()} {self.user_tr.get_currency()} ({self.user_tr.get_actual_amount():.2f} USD) потрачено на {reason}. Остаток на счете: {self.user.get_total():.2f} USD.")
                else:
                    await update.message.reply_text("Недостаточно средств на счете или счет не был пополнен.")
            else:
                await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron) и причину.")

        else:
            await update.message.reply_text("Неправильный ввод. Попробуйте снова.")
        
        
        

    # Команда /balance - проверка баланса
    async def balance(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        

        if self.user.get_total() > 0:
            await update.message.reply_text(f"Ваш баланс: {self.user.get_total()} : USD")
        else:
            await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")


    #  Команда /spendings показывающая список растрат
    async def spendings(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        counter= 1

        if len(self.user_tr.get_expences()) > 0 :
            await update.message.reply_text("Вот список ваших растрат :")
            for i in range(len(self.user_tr.get_expences())):
                await update.message.reply_text(f"{counter} {self.user_tr.get_expence(i)} USD потрачено на {self.user_tr.get_reason(i)}")
                counter +=1
        else:
            await update.message.reply_text("У вас пока что нет никаких растрат.Нажмите /spend что бы потратить деньги )")
        