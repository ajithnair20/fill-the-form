from rules.irule import IRule
from rules.type_detect_rule import TypeFromLabelRule, TypeFromInputRule
from rule_generator.input_text_rule_generator import InputTextRuleGenerator


class InputElementRule(IRule):
    rule_list = [TypeFromInputRule(), TypeFromLabelRule()]
    rule_generator = InputTextRuleGenerator()

    def compute_text(self, *args):
        input_element_dict = args[0]
        label_element_dict = args[1]
        error_message = '' if len(args) < 3 else args[2]
        falsify_inputs = True if len(args) < 4 else args[3]
        type_value = 'text_input'

        for rule in self.rule_list:
            text = rule.determine_type(input_element_dict, label_element_dict)
            if len(text) > 0:
                type_value = (text + '_input')
                break

        input_text_rule = self.rule_generator.generate_rule(type_value)
        return input_text_rule.determine_input_text(input_element_dict, label_element_dict, error_message, falsify_inputs)
