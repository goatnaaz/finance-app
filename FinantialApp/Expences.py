from UserTransactions import UserTr
from telegram import Update,ReplyKeyboardMarkup

class Expences (UserTr):
    __expences= []
    __reasons= []

    def set_expences(self,num):
        self.__expences.append(num)

    def get_reasons(self,num):
        return self.__reasons[num]

    def set_reasons(self,text):
        self.__reasons.append(text)

    def get_expences_by_index(self,num):
        return self.__expences[num]
    
    def get_expences(self):
        return self.__expences
    
    def get_expences_length(self):
        return len(self.__expences)
    
    

    
    
