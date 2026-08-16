def check_type(usr_input, allow_type):
    if allow_type is str:
        return usr_input
    
    try:
        return allow_type(usr_input)
    except (ValueError, TypeError):
        print(f'Invalid, {usr_input} is not a valid {allow_type.__name__}')
        return None

    
def take_input(text = "", allow_type = str, case_sensitive = True, choices = None, rule = lambda x: True, rule_error = "Rule violated"):
    '''
    input() module with extended capabilities like type checking, 
    case sensitive check, choices list and custom rules
    '''
    while True:
        usr_input = input(text)
        converted = check_type(usr_input, allow_type)
            
        if converted is None:
            continue
        try:
            rule_valid = rule(converted)
        except ValueError:
            print(rule_error)
            continue

        if not rule_valid:
            print(rule_error)
            continue

        if allow_type is not str:
            return converted

        # str
        if not choices:
            return usr_input
        if not case_sensitive:
            usr_input = usr_input.lower()
            choices = [item.lower() for item in choices]

        if usr_input in choices:
            return usr_input
        else:
            print(f'Invalid, please choose between ({", ".join(choices)})')
            continue
