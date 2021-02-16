from rules.input_text_rule import NumberInputTextRule, TelInputTextRule, PasswordInputTextRule, EmailInputTextRule, \
    RangeInputTextRule, UsernameInputTextRule, GenericInputTextRule, DateInputTextRule


class InputTextRuleGenerator:
    def generate_rule(self, service_context: str):
        if service_context == 'number_input':
            return NumberInputTextRule()
        elif service_context == 'tel_input':
            return TelInputTextRule()
        elif service_context == 'password_input':
            return PasswordInputTextRule()
        elif service_context == 'email_input':
            return EmailInputTextRule()
        elif service_context == 'range_input':
            return RangeInputTextRule()
        elif service_context == 'username_input':
            return UsernameInputTextRule()
        elif service_context == 'text_input':
            return GenericInputTextRule()
        elif service_context == 'date_input':
            return DateInputTextRule()
