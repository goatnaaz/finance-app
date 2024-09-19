from Entities.Exchange import Exchange


class UserTr():
    """Класс для сохранения транзакицй пользователя"""

    
    __amount= 0
    __currency= ''
    __actual_amount= 0
    
    __expences= []
    __reasons= []

    
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
        self.__expences.append(expence)

    def get_expences(self):
        return self.__expences
    
    def get_expence(self,num):
        return self.__expences[num]
    
    def set_reason(self,reason):
        self.__reasons.append(reason)

    def get_reasons(self):
        return self.__reasons
    
    def get_reason(self,num):
        return self.__reasons[num]

    def get_actual_amount(self):
        return self.__actual_amount
    
    def create_actual_amount(self,currency,amount):
        self.__currency= currency
        self.__amount= amount

        for i in self._exchange_rates:
            if i.get_name() == currency:
                self.__actual_amount= self.__amount * i.get_value()
        





