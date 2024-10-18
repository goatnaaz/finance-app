from Entities.Exchange import Exchange


class UserTr():
    """Класс для сохранения транзакицй пользователя"""

    
    __amount= 0
    __currency= ''
    __actual_amount= 0
    
    __expence= 0
    __reason= ''

    
    _exchange_rates= [Exchange('usd',1.0),Exchange('eur',1.1),Exchange('uah',0.027),Exchange('ron',0.22)]
   

    def is_in_exchange_rates(self,exchange_name):

        for i in self._exchange_rates:
            if i.get_name() == exchange_name:
                return  True
        else:
            return False

    
    def set_amount(self,amount):
        self.__amount= amount

    def get_amount(self):
        return self.__amount
    
    def set_currency(self,currency):
        self.__currency= currency

    def get_currency(self):
        return self.__currency
    
    def set_expence(self,expence):
        self.__expence= expence

    
    def get_expence(self):
        return self.__expence
    
    def set_reason(self,reason):
        self.__reason= reason

    def get_reason(self):
        return self.__reason
    

    def get_actual_amount(self):
        return self.__actual_amount
    
    def create_actual_amount(self,currency,amount):
        self.__currency= currency
        self.__amount= amount

        for i in self._exchange_rates:
            if i.get_name() == currency:
                self.__actual_amount= self.__amount * i.get_value()

    def is_expense(self):
        if self.__expence > 0 and len(self.__reason) > 0:
            return True
        else:
            return False
        





