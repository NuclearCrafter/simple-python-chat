class telegram:
    def __init__(self,header='',message='',arguments=''):
        self.header = header
        self.message = message
        self.arguments = arguments

class telegram_parser:
    def parse_telegram(self,text):
        if text[0] == '#':       
            splitted = text.split(':')
            header = splitted[0]
            message = ''.join(splitted[2:])
            arguments = splitted[1].split(',')
            telegram_received = telegram(header,message,arguments)
        else:
            telegram_received = telegram('#MSG',text,['Server','debug'])
        return telegram_received

