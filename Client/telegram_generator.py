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

    def generate_message_string(self, message_type, message, arguments=['']):
        message_type_string = message_dictionary[message_type.value]
        if type(arguments) == str:
            argstring = arguments
        else:
            argstring = ','.join(arguments)
        message_string = '#MSG:'+message_type_string+','+argstring+':'+message
        return message_string
    def generate_login_string(self,arguments=['']):
        argstring = ','.join(arguments)
        message_string = '#LGN:credentials,'+argstring+':'
        return message_string
    def generate_check_login(self):
        return '#LGN:status:'
    def generate_telegram(self, teleg_type, text, message_type, arguments=['']):
        if teleg_type == telegram_types.MSG:
            message = self.generate_message_string(message_type,text,arguments)
        elif teleg_type == telegram_types.LGN:
            message = self.generate_message_string(arguments)
        return message

generator = telegram_generator()

#print(message_dictionary[1])
#print(generator.generate_telegram(telegram_types.MSG,'hello',message_types.broadcast))