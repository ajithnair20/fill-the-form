from xeger import Xeger

class PhoneNumberGenerator:
    def __init__(self):
        self.phoneFormats = {
            'US': ('+1',['\+1\s*\([\da-zA-Z]{3}\)-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}', '\+*1*\s*\([\da-zA-Z]{3}\)-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}', '\+*1*\s*\([\da-zA-Z]{3}\)-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}', '\+*1*\s*\(*[\da-zA-Z]{3}\)*-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}', '\+1\s*\(*[\da-zA-Z]{3}\)*-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}', '\+*1*\s*\(*[\da-zA-Z]{3}\)*-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}']),
            'IN':('+91',['+91\s*[9876]{1}[0-9]{9}','\+*9*1*\s*[9876]{1}[\d]{9}']),
            'KN':('+254',9),
            'SA':('+27',10),
            'CH':('+86 ',10),
            'HK':('+852',8),
            'IR':('+98',11),
            'JP':('+81',11),
            'ML':('+60',9),
            'PK':(),
        }

    def getPhoneNumber(self, country_code, *digits):
        res = []
        if country_code in self.phoneFormats:
            country_regex = self.phoneFormats[country_code]
            try:
                x = Xeger()
                op = x.xeger(country_regex)
                res = [op]
            except Exception:
                print('Error generating input string based on the regex')
                # Return default tel 
                return '9876543210'
        return res