
import random


#класс для данных юзера
class User ():

    __id= 0
    __chat_id= 0
    __total_amount_in_defauld_currency= 0
    __user_transactions = []
    


    def get_id(self):
        return self.__id
    
    def set_chat_id(self,chat_id):
        self.__chat_id= chat_id

    def get_chat_id(self):
        return self.__chat_id
    

    def add(self,UserTr):
        
        self.__total_amount_in_defauld_currency += UserTr.get_actual_amount()

    def subtract(self,UserTr):
        self.__total_amount_in_defauld_currency -= UserTr.get_actual_amount()

    def get_total(self):
        return self.__total_amount_in_defauld_currency

    def add_user_tr(self,UserTr):
        self.__user_transactions.append(UserTr)

    def get_user_tr(self):
        return self.__user_transactions
