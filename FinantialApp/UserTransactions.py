import random

class UserTr():
    """Класс для сохранения транзакицй пользователя"""

    __id= random.randrange(0,101) #уникальный id
    __user_id= 0 # id но взятый из чата пользователя с ботом
    __amount= 0 # сумма введенная пользователем
    __user_currency= '' # валюта введенная пользователем
    __actual_amount= 0 # сумма после перевода в доллары
    __created_at= '' #


    def get_id(self):
        return self.__id
    
    def get_user_id(self):
        return self.__user_id
    
    def set_user_id(self,user_id):
        self.__user_id= user_id

    def get_amount(self):
        return self.__amount
    
    def set_amount(self,amount):
        self.__amount= amount

    def get_user_currency(self):
        return self.__user_currency
    
    def set_user_currency(self,user_currency):
        self.__user_currency= user_currency

    def get_actual_amount(self):
        return self.__actual_amount
    
    def set_actual_amount(self,actual_amount):
        self.__actual_amount= actual_amount

    def get_created_at(self):
        return self.__created_at
    
    def set_created_at(self,created_at):
        self.__created_at= created_at





