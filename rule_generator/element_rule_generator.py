from rules.input_element_rule import InputElementRule


class ElementRuleGenerator:
    def generate_rule(self, service_context: str):
        if service_context == 'input':
            return InputElementRule()
