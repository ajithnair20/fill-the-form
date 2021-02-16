"""
File with different HTML input field formats and methods to fetch valid input for a given error message 
Ignoring Obselete HTML input formats such as Datetime

Valid Input Categories:
key: Desc
tel: telephone -> Pass the valid regular expression pattern along with error message 
date: Date -> Pass the error message with optional parameter with value 'past' or 'future'
phone: Phone number -> pass error message string with optional country code
tel: Telephoen number -> Pass the regex pattern in the pattern attribute of the input
username: Username -> Pass the error message with optional parameter - username that was previously entered
"""

from datetime import datetime
from xeger import Xeger
import string 
import random
import nltk
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import word_tokenize
import re
import os
from word2number import w2n

from utilities.utilities import getSentenceSentiment

nltk.download('punkt')

# Date format pairs
formats = {'mm-dd-yy': '%m-%d-%y',
           'mm-dd-yyyy': '%m-%d-%Y',
           'dd-mm-yy': '%d-%m-%y',
           'dd-mm-yyyy': '%d-%m-%Y',
           'yy-dd-mm': '%y-%d-%m',
           'yyyy-dd-mm': '%Y-%d-%m',
           'mm/dd/yy': '%m/%d/%y',
           'mm/dd/yyyy': '%m/%d/%Y',
           'dd/mm/yy': '%d/%m/%y',
           'dd/mm/yyyy': '%d/%m/%Y',
           'yy/dd/mm': '%y/%d/%m',
           'yyyy/dd/mm': '%Y/%d/%m', }

ph_formats = {
    '\+1\s*\([\da-zA-Z]{3}\)-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}' :  '+1(123)-456-7890',
    '\+*1*\s*\([\da-zA-Z]{3}\)-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}' :  '(123)-456-7890', 
    '\+*1*\s*\([\da-zA-Z]{3}\)-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}' : '(123)4567890',
    '\+*1*\s*\(*[\da-zA-Z]{3}\)*-\s*[\da-zA-Z]{3}-\s*[\da-zA-Z]{4}' : '123-456-7890',
    '\+1\s*\(*[\da-zA-Z]{3}\)*-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}' : '+11234567890',
    '\+*1*\s*\(*[\da-zA-Z]{3}\)*-*\s*[\da-zA-Z]{3}-*\s*[\da-zA-Z]{4}':  '1234567890'
}

# Range keywords
min_keywords = ['least','min','minimum']
max_keywords = ['most', 'max', 'maximum']
range_keywords = ['between']
random_username_suffix = ['randomizedsuffix134']

# enter the paths to the Stanford POS Tagger .jar file as well as to the model to be used
dirname = os.path.dirname(__file__)
jar = os.path.join(dirname, '../corenlp/stanford-postagger-full-2020-11-17/stanford-postagger.jar')
model = os.path.join(dirname, '../corenlp/stanford-postagger-full-2020-11-17/models/english-bidirectional-distsim.tagger')


# Method to get date input for the given message
def getDateInput(string):
    # Fetch current date time
    dt = datetime.now()
    # check if date from the past is required
    # TODO: Check future and past references and date range in the error message 
    # check for references to future - after, within,  
    # if (len(args) > 0):
    #     date_type = args[0]
    #     if date_type == 'past':
    #         dt = datetime.now() - relativedelta(years=19)
    #     elif date_type == 'future':
    #         dt = datetime.now() + relativedelta(months=1)

    date_formats = formats.keys()
    for fmt in date_formats:
        if fmt in string:
            return dt.strftime(formats[fmt])
    # Return current date in mm-dd-yyyy format by default 
    return dt.strftime("%Y-%m-%d")  # Standard HTML 5 ISO8601 format


# Method to get phone number input for the given message
def getPhoneNumberInput(string):
    # Fetch current date time   
    us_phone_formats = ph_formats.keys()
    for fmt in us_phone_formats:
        x = re.search(fmt, string)
        if x:
            return ph_formats[fmt]
    # Return 10 digit number by default 
    return '9876543210'


# Method to get email input for the given message
def getEmailInput():
    # Return default email 
    return 'scoobydoo123doobody@gmail.com'


# Method to get email input for the given message
def getColorInput():
    # Return default email 
    return '#000000'

# Method to get input for tel input based on regex
def getTelInput(regex_str):
    try:
        x = Xeger()
        op = x.xeger(regex_str)
        return op
    except Exception:
        print('Error generating input string based on the regex')
        # Return default tel 
        return '9876543210'

# Method to get username based on error messaage
def getUsername(message, *args):
    pos_tagger = StanfordPOSTagger(model, jar, encoding = "utf-8")
    words = nltk.word_tokenize(message.lower())
    tagged_words = pos_tagger.tag(words)
    sug_usernames = []
    # Check if pervious username input is passed
    if len(args) > 0:
        previous_username = args[0]
        sug_usernames = [word for word,tag in tagged_words if tag in ['NN', 'NNP', 'FW', 'NNPS'] and word != previous_username]
    else:
        sug_usernames = [word for word,tag in tagged_words if tag in ['NN', 'NNP', 'FW', 'NNPS']]

    if len(sug_usernames) > 0:
        if getSentenceSentiment(message) == 'pos':
            return sug_usernames[-1]
        else:
            return sug_usernames[-1] + 'salt123' # return last suggested username

    return 'randomuser567user'

# Method to get Age based on error message
def getAgeInput(string):
    return '23'

# Method to get Age based on error message
def getDayInput(string):
    return '18'

# Method to get Age based on error message
def getMonthInput(string):
    return 'Aug'

# Method to get Age based on error message
def getYearInput(string):
    return '1983'

#Method to get zipcode based on error message
def getZipcodeInput(string):
    try:
        valid_zip_regex = '^[0-9]{5}(?:-[0-9]{4})?$'
        x = Xeger()
        op = x.xeger(valid_zip_regex)
        return op
    except Exception:
        print('Error generating value from regex')
    
    return '20001' # Default value DC zipcode
    

# Method to infer range, minimum and maximum from the error message / placeholder

def get_min_max_val(message, range_type):
    index = -1
    tokens = word_tokenize(message)
    window_size = 3

    keywords=[]
    if range_type == 'min':
        keywords = min_keywords
    else:
        keywords = max_keywords

    # Check if min/max keywords exist in the message
    for word in keywords:
        if word in message:
            index = tokens.index(word)
            break
    
    # In case yes then find the number of characters/numbers from the message within the window
    if index >= 0:
        start = (0, index-window_size)[index - window_size >=0]
        end = (len(tokens)-1, index+window_size)[index + window_size < len(tokens)]

        num=-1

        #extract the digit from the message within the window
        sub_msg = "".join(tokens[start:end+1])
        m = re.search(r'\d+', sub_msg)
        if m:
            num = int(m.group(0))
        
        if num  == -1:
            #check if the number is in word
            try:
                num = int(w2n.word_to_num(sub_msg))
            except Exception as e:
                print(e)

        if num > 0:
            #check if characters are required
            if 'character' in message:
                x = Xeger()
                op = x.xeger('[a-zA-Z0-9]{'+ str(num) +'}')
                return op
        else:
            return ''

    else:
        return ''

def inferRange(message):
    min_str = get_min_max_val(message,'min')
    max_str = get_min_max_val(message,'max')

    return (min_str, (max_str, '')[max_str == ''])[min_str == '']

def generateInputValue(element, label, error_msg=''):

    element_attr = element['input_attributes']

    # Check input element for regex to validate the input
    if 'pattern' in element_attr:
        try:
            regex_str = element_attr['pattern']
            x = Xeger()
            op = x.xeger(regex_str)
            return op
        except Exception:
            print('Error generating value from regex')

    input_val = inferRange(error_msg)
    if input_val != '':
        return input_val

    # search_str = error_msg + ' ' + (' ', element_attr['placeholder'])['placeholder' in element_attr] + ' ' + (' ', element_attr['type'])['type' in element_attr]
    search_str = str(error_msg) + ' ' + str(element['element']) + ' ' + str(label)
    search_str = search_str.lower()

    if 'date' in search_str:
        return getDateInput(search_str)

    elif 'phone' in search_str or 'mobile' in search_str or 'tel' in search_str:
        return getPhoneNumberInput(search_str)

    elif 'zip' in search_str or 'pincode' in search_str or 'zipcode' in search_str:
        return getZipcodeInput(search_str)

    elif 'age' in search_str:
        return getAgeInput(search_str)

    elif 'day' in search_str:
        return getDayInput(search_str)

    elif 'month' in search_str:
        return getMonthInput(search_str)

    elif 'year' in search_str:
        return getYearInput(search_str)

    elif 'username' in search_str:
        return getUsername(error_msg)

    elif 'color' in search_str:
        return getColorInput()

    elif 'email' in search_str:
        return getEmailInput()

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 