class Exchange():
    _currency_name= None
    _value= None

    def __init__(self,currency_name,value) -> None:
        self._currency_name= currency_name
        self._value= value

    def get_name(self):
        return self._currency_name
    
    def get_value(self):
        return self._value