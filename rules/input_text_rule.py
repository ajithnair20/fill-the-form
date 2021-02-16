import random

from utilities.patterns import generateInputValue

class InputTextRule:
    false_input_text_dict = {
        'FALSE_PASSWORD': 'bb',
        'FALSE_EMAIL': 'abc',
        'FALSE_NUMBER': -2,
        'FALSE_MONTH': -2,
        'FALSE_YEAR': -1000,
        'FALSE_TEL': '6789',
        'FALSE_USERNAME': 'abc',
        'FALSE_RANGE': 34
    }

    generated_password = ''

    def determine_input_text(self, *args):
        pass


class GenericInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return 'abc'
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class DateInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return 'abc'
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class EmailInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_EMAIL']
        else:
            return 'scoobydoo123doobody@gmail.com'


class TelInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_TEL']
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class RangeInputTextRule(InputTextRule):

    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_RANGE']
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class NumberInputTextRule(InputTextRule):
    min, max = 5, 1000

    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_NUMBER']
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class MonthInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args[2]) < 3 else args[2]
        falsify_inputs = True if len(args[3]) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_MONTH']

        return random.choice(range(1, 13))


class UsernameInputTextRule(InputTextRule):
    def determine_input_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_USERNAME']
        else:
            return generateInputValue(input_element_dict, label_element_dict, error_msg=error_message)


class PasswordInputTextRule(InputTextRule):
    password_chars_dict = {
        "possible_characters_upper_case": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "possible_characters_lower_case": "abcdefghijklmnopqrstuvwxyz",
        "possible_digits": "0123456789",
        "possible_special_characters": "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    }

    # accepted minimum length of a password to guard against offline attacks
    min_length = 18

    def determine_input_text(self, *args):
        input_element_dict = args[0]
        attributes_dict = input_element_dict['input_attributes']
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]

        if falsify_inputs:
            return self.false_input_text_dict['FALSE_PASSWORD']
        elif falsify_inputs is False and len(InputTextRule.generated_password) > 0:
            return InputTextRule.generated_password

        if 'minlength' in attributes_dict.keys():
            self.min_length = int(attributes_dict['minlength'])

        min_length = int(self.min_length)
        dict_len = len(self.password_chars_dict.keys())
        lengths = []
        for i in range(1, dict_len + 1):
            if i == dict_len:
                lengths.append(min_length)
            else:
                lengths.append(self.min_length // dict_len)
            min_length -= self.min_length // dict_len

        chosen_chars = ''

        for length, key in zip(lengths, self.password_chars_dict.keys()):
            value = self.password_chars_dict[key]
            if length > len(value):
                while length > len(value):
                    value += value
            chosen_chars += ''.join(random.sample(value, length))

        InputTextRule.generated_password = ''.join(random.sample(chosen_chars, len(chosen_chars)))
        return InputTextRule.generated_password
