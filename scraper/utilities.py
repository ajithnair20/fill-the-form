def extract_nearest_sibling_element_by_tag(element, element_tag, is_before):
    if not is_before:
        for sibling in element.next_siblings:
            if sibling.name == element_tag:
                return sibling
    else:
        for sibling in element.previous_siblings:
            if sibling.name == element_tag:
                return sibling
