from UserTransactions import UserTr
from Expences import Expences

class User (Expences):
    
    __id= 0
    __chat_id= 0
    __total_amount_in_defauld_currency= 0
    __transactions= [] 
    
    

    def get_id(self):
        return self.__id

    def get_chat_id(self):
        return self.__chat_id
    
    def set_chat_id(self,chat_id):
        self.__chat_id= chat_id

    
    def add(self,UserTr):
        self.__id= UserTr.get_id()
        self.__chat_id= UserTr.get_user_id()
        self.__transactions.append(int(UserTr.get_actual_amount()))



    def get_total(self):

        self.__total_amount_in_defauld_currency= 0
        exp= Expences().get_expences()

        for i in range(len(self.__transactions)):
            self.__total_amount_in_defauld_currency += self.__transactions[i]

        for i in exp:
            self.__total_amount_in_defauld_currency -= i

        return self.__total_amount_in_defauld_currency
