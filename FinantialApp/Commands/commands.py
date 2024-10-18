
from Entities.UserTransactions import UserTr
from Entities.User import User
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from Commands.TransactionHandler import TransactionHandler
from Services.balanceServices import BalanceServise



#класс комманд для телеграм бота
class Commands():

    
    reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    _users= []
    _balance_servise= BalanceServise()
    
    #  Команда /start для преведствования пользователя и ознакомления с функционалом
    async def start(self,update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:

        chat_id = update.message.chat_id
        user= None

        if len(self._users) == 0 :
            user= User()
            user.set_chat_id(chat_id)
            self._users.append(user)
        else:
            for i in self._users:
                if i.get_chat_id() == chat_id:
                    user= i
                else:
                    user= User()
                    user.set_chat_id(chat_id)
                    self._users.append(user)

    
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
        chat_id = update.message.chat_id
        user= self._balance_servise.check_user(self._users,chat_id)

        if user == None:
            await update.message.reply_text("Сначала нажмите кнопку /start прежде чем использовать друшие комманды")
        else:

            text = update.message.text.split()

            if len(text) == TransactionHandler.DEPOSIT.value:  # Пополнение счета
            
                user_tr= UserTr()
                amount_str, currency = text

                user_tr= self._balance_servise.deposit(user_tr,user,amount_str,currency)

                if user_tr != None:
                    await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_currency()} конвертировано и добавлено на ваш счет как {user_tr.get_actual_amount():.2f} USD!")
            
                else:

                    await update.message.reply_text("Неправильный ввод. Введите сумму и валюту (usd, eur, grn, ron).")

            elif len(text) >= TransactionHandler.SPEND.value :  # Учет расходов
                user_tr= UserTr()
                amount_str, currency, *reason = text
                reason = ' '.join(reason) 

                user_tr= self._balance_servise.spend(user_tr,user,amount_str,currency,reason)

                if user_tr != None:
                    
                    await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_currency()} ({user_tr.get_actual_amount():.2f} USD) потрачено на {user_tr.get_reason()}. Остаток на счете: {user.get_total():.2f} USD.")
                else:
                    await update.message.reply_text("Недостаточно средств на счете или счет не был пополнен.")
                    await update.message.reply_text(" Проверьте счет с помощью комманды /balance или проверьте ваш вод данных")
                
            else:
                await update.message.reply_text("Неправильный ввод. Попробуйте снова.")
        
        
        

    # Команда /balance - проверка баланса
    async def balance(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        user= self._balance_servise.check_user(self._users,chat_id)

        
        if user == None:
            await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")
        elif user != None:
            if user.get_total() > 0 :
                await update.message.reply_text(f"Ваш баланс: {user.get_total()} : USD")
            else:
                await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")



    #  Команда /spendings показывающая список растрат
    async def spendings(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        counter= 1
        chat_id = update.message.chat_id
        user= self._balance_servise.check_user(self._users,chat_id)


        transactions= user.get_user_transactions()
        
        if user.is_spend_transactions():
            await update.message.reply_text('Список всех ваших растрат :')
            for i in transactions:
                if i.is_expense() :
                    await update.message.reply_text(f"{counter} : {i.get_expence()} USD было потрачено на {i.get_reason()}")
                    counter += 1
        else:
            await update.message.reply_text("У вас пока что нет никаких растрат")

        
        