
from Entities.UserTransactions import UserTr
from Entities.User import User
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from Commands.TransactionHandler import TransactionHandler
from Services.BalanceService import BalanceService



#класс комманд для телеграм бота
class Commands():
    reply_keyboard = [
    ["/balance", "/deposit"],
    ["/spend", "/spendings"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    _users = []
    balance_service = BalanceService()
 
    
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

        user = None
        #TODO: Check if user already exists
        #If user exists, get user by chat_id
        #If user does not exist, create new user

        #Here we gonna check if user already exists in our static users list
        #if userFromList.get_chat_id() == update.message.chat_id:
            #user = userFromList

        #This will create a new user and append in our static users list
        #if user is None
        user = User()
        user.set_chat_id(update.message.chat_id)
        self._users.append(user)

        self.balance_service.check_method()

        text = update.message.text.split()



        if len(text) == TransactionHandler.DEPOSIT.value:  # Пополнение счета

            amount_str, currency = text

            if amount_str.isdigit() and currency.lower() in self.user_tr.get_exchange():
                user_tr = UserTr()
                user_tr.create_actual_amount(currency,float(amount_str))

                self.user.add(self.user_tr)
                self.user.add_user_tr(user_tr)

                await update.message.reply_text(f"{user_tr.get_amount()} {user_tr.get_currency()} конвертировано и добавлено на ваш счет как {user_tr.get_actual_amount():.2f} USD!")
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

        self.balance_service.balance()

        if self.user.get_total() > 0:
            await update.message.reply_text(f"Ваш баланс: {self.user.get_total()} : USD")
        else:
            await update.message.reply_text("Ваш баланс пуст. Пожалуйста, пополните счет с помощью команды /deposit.")


    #  Команда /spendings показывающая список растрат
    async def spendings(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        counter= 1
        self.balance_service.spend()
        if len(self.user_tr.get_expences()) > 0 :
            await update.message.reply_text("Вот список ваших растрат :")
            for i in range(len(self.user_tr.get_expences())):
                await update.message.reply_text(f"{counter} {self.user_tr.get_expence(i)} USD потрачено на {self.user_tr.get_reason(i)}")
                counter +=1
        else:
            await update.message.reply_text("У вас пока что нет никаких растрат.Нажмите /spend что бы потратить деньги )")
        