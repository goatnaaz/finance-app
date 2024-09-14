import random


class UserTr():
    """Класс для сохранения транзакицй пользователя"""

    __amount = 0
    __currency = ''
    __actual_amount = 0
    __expences = []
    __reasons = []

    # Курс валют по отношению к доллару
    exchange_rates = {
        'usd': 1.0,  # курс доллара к доллару
        'eur': 1.1,  # курс евро к доллару (примерный)
        'grn': 0.027,  # курс гривны к доллару (примерный)
        'ron': 0.22  # курс румынского лея к доллару (примерный)
    }

    def get_exchange(self):
        return self.exchange_rates

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_currency(self, currency):
        self.__currency = currency

    def get_currency(self):
        return self.__currency

    def set_expence(self, expence):
        self.__expences.append(expence)

    def get_expences(self):
        return self.__expences

    def get_expence(self, num):
        return self.__expences[num]

    def set_reason(self, reason):
        self.__reasons.append(reason)

    def get_reasons(self):
        return self.__reasons

    def get_reason(self, num):
        return self.__reasons[num]

    def get_actual_amount(self):
        return self.__actual_amount

    def create_actual_amount(self, currency, amount):
        self.set_currency(currency)
        self.set_amount(amount)
        self.__actual_amount = self.get_amount() * self.exchange_rates[currency.lower()]


User.user_transactions = [UserTr(), UserTr(), UserTr()];
