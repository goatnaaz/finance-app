
from Entities.UserTransactions import UserTr
from Entities.User import User
from telegram import Update
from telegram.ext import ContextTypes
from Commands.TransactionHandler import TransactionHandler

class BalanceServise ():

    def check_user(self,users,chat_id):

        for i in users:
            if i.get_chat_id() == chat_id:
                return i
            else:
                return None 

    def deposit(self,user_tr,user,amount,currency):
        if amount.isdigit() and user_tr.is_in_exchange_rates(currency.lower()):

            user_tr.create_actual_amount(currency,float(amount))
            user.add(user_tr)
            user.add_user_tr(user_tr)

            return user_tr
        else:
            return None

        
    def spend(self,user_tr,user,amount,currency,reason):
        if amount.isdigit() and user_tr.is_in_exchange_rates(currency.lower()) == True:

            if user.get_total() > 0:

                user_tr.create_actual_amount(currency,float(amount))
                user_tr.set_reason(reason)
                user_tr.set_expence(user_tr.get_actual_amount())
                
                user.subtract(user_tr)
                user.add_user_tr(user_tr)

                return user_tr
            else:
                return None
        else:
            return None
    
    
        
