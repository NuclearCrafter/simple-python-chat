class telegram:
    def __init__(self,header='',message='',arguments=''):
        self.header = header
        self.message = message
        self.arguments = arguments

class telegram_parser:
    def parse_telegram(self,text):       
        splitted = text.split(':')
        header = splitted[0]
        message = ''.join(splitted[2:])
        arguments = splitted[1].split(',')
        telegram_received = telegram(header,message,arguments)
        return telegram_received

