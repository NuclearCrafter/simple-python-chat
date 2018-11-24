from enum import Enum

class telegram_types(Enum):
    MSG = 1
    LGN = 2

class message_types(Enum):
    broadcast = 1
    private = 2
    group = 3

message_dictionary = {1:'broadcast',2:'private',3:'group'}

class telegram_generator:

    def generate_message_string(self, message_type, message, receiver = ''):
        message_type_string = message_dictionary[message_type.value]
        message_string = '#MSG:'+message_type_string+','+receiver+':'+message
        return message_string

    def generate_telegram(self, teleg_type, text, message_type, receiver = ''):
        if teleg_type == telegram_types.MSG:
            message = self.generate_message_string(message_type,text,receiver)
        elif teleg_type == telegram_types.LGN:
            pass
        return message

generator = telegram_generator()

#print(message_dictionary[1])
#print(generator.generate_telegram(telegram_types.MSG,'hello',message_types.broadcast))