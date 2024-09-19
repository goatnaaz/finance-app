
from Entities.UserTransactions import UserTr
from Entities.User import User
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from Commands.TransactionHandler import TransactionHandler



#класс комманд для телеграм бота
class Commands():

    
    reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    _users= []
 
    
    #  Команда /start для преведствования пользователя и ознакомления с функционалом
    async def start(self,update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:

    
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

        user= None

        if self._users:
            for i in self._users:
                if i.get_chat_id() == update.message.chat_id:
                    user= i
                else:
                    user= User()
            user.set_chat_id(update.message.chat_id)
            self._users.append(user)
        else:
            user= User()
            user.set_chat_id(update.message.chat_id)
            self._users.append(user)

        text = update.message.text.split()

        if len(text) == TransactionHandler.DEPOSIT.value:  # Пополнение счета
            
            user_tr= UserTr()
            amount_str, currency = text

            if amount_str.isdigit() and user_tr.is_in_exchange_rates(currency.lower()):

                

                user_tr.create_actual_amount(currency,float(amount_str))
                user.add(user_tr)
                user.add_user_tr(user_tr)



                await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_currency()} конвертировано и добавлено на ваш счет как {user_tr.get_actual_amount():.2f} USD!")
            else:
                await update.message.reply_text(currency.lower())
                await update.message.reply_text(user_tr.is_in_exchange_rates(currency.lower))
                await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron).")

        elif len(text) >= TransactionHandler.SPEND.value :  # Учет расходов
            user_tr= UserTr()
            amount_str, currency, *reason = text
            reason = ' '.join(reason) 

            if amount_str.isdigit() and user_tr.is_in_exchange_rates(currency.lower()) == True:

                if self.user.get_total() > 0:

                    
                    
                    user_tr.create_actual_amount(currency,float(amount_str))
                    user_tr.set_reason(reason)
                    user_tr.set_expence(user_tr.get_actual_amount())
                
                    user.subtract(user_tr)

                    user.add_user_tr(user_tr)
                    
                    await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_currency()} ({user_tr.get_actual_amount():.2f} USD) потрачено на {reason}. Остаток на счете: {user.get_total():.2f} USD.")
                else:
                    await update.message.reply_text("Недостаточно средств на счете или счет не был пополнен.")
            else:
                await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron) и причину.")

        else:
            await update.message.reply_text("Неправильный ввод. Попробуйте снова.")
        
        
        

    # Команда /balance - проверка баланса
    async def balance(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        
        user= None
        for i in self._users:
            if i.get_chat_id() == chat_id:
                user= i
                if user.get_total() > 0:
                    await update.message.reply_text(f"Ваш баланс: {user.get_total()} : USD")   
                else:
                    await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")
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
        