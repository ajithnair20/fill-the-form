from rules.irule import IRule
from schema.schema import build_schema
from nltk.corpus import stopwords

input_element_possible_types = {
    'email',
    'tel',
    'username',
    'number',
    'password',
    'range',
    'time',
    'url',
    'week',
    'radio',
    'date'
}

input_element_possible_attrs = {
    'pattern',
    'name',
    'placeholder',
    'size',
    'minlength',
    'maxlength'
}

form_specific_stop_words = {
    'please',
    'enter',
    'valid',
    'create',
    'your',
    'confirm',
    'fill'
}

stop_words = set(stopwords.words('english'))

stop_words |= form_specific_stop_words


class TypeDetectRule(IRule):
    def determine_type(self, *args):
        pass


class TypeFromLabelRule(TypeDetectRule):
    def determine_type(self, *args):
        label_element_dict = args[1]
        if label_element_dict:
            for specific_type in input_element_possible_types:
                for key in label_element_dict['label_attributes']:
                    if type(label_element_dict['label_attributes'][key]) is str:
                        if specific_type in label_element_dict['label_attributes'][key]:
                            return specific_type
        return ''


class TypeFromInputRule(TypeDetectRule):
    def determine_type(self, *args):
        input_element_dict = args[0]
        if input_element_dict:
            if input_element_dict['input_attributes']['type'] in input_element_possible_types:
                return input_element_dict['input_attributes']['type']
            else:
                for specific_type in input_element_possible_types:
                    for key in input_element_dict['input_attributes'].keys():
                        if type(input_element_dict['input_attributes'][key]) is str:
                            if specific_type in input_element_dict['input_attributes'][key].lower():
                                return specific_type
        return ''


class TypeFromErrorMessageRule(TypeDetectRule):
    def determine_type(self, *args):
        type_from_label_rule = TypeFromLabelRule()
        type_from_input_rule = TypeFromInputRule()

        determined_input = None
        determined_label = None

        error_element = args[0]
        error_text = str(args[1]).lower()
        error_text_strings = error_text.split()
        filter_error_text_strings = [string for string in error_text_strings if not string in stop_words]

        previous_input_elements = error_element.find_all_previous(name='input')
        previous_label_elements = error_element.find_all_previous(name='label')
        next_input_elements = error_element.find_all_next(name='input')
        next_label_elements = error_element.find_all_next(name='label')

        for previous_input_element in previous_input_elements:
            for error_text_string in filter_error_text_strings:
                if error_text_string.lower() in str(build_schema(previous_input_element, 'input')['element']).lower():
                    determined_input = previous_input_element
                    break
            if determined_input:
                break


        for previous_label_element in previous_label_elements:
            for error_text_string in filter_error_text_strings:
                if error_text_string.lower() in str(build_schema(previous_label_element, 'label')['element']).lower():
                    determined_label = previous_label_element
                    break
            if determined_label:
                break


        if determined_label is None:
            determined_label = None if len(previous_label_elements) == 0 else previous_label_elements[0]

        if determined_input is None:
            determined_input = None if len(previous_input_elements) == 0 else previous_input_elements[0]


        if determined_input is None:
            for next_input_element in next_input_elements:
                for error_text_string in filter_error_text_strings:
                    if error_text_string.lower() in str(build_schema(next_input_element, 'input')['element']).lower():
                        determined_input = next_input_element
                        break
                if determined_input:
                    break

        if determined_label is None:
            for next_label_element in next_label_elements:
                for error_text_string in filter_error_text_strings:
                    if error_text_string.lower() in str(build_schema(next_label_element, 'label')['element']).lower():
                        determined_label = next_label_element
                        break
                if determined_label:
                    break

        return determined_input, determined_label
