def take_input(text: str = "", allow_type: type = str, case_sensitive: bool = False,
          choices = None, rule = lambda x: True, rule_error: str = "rule violated"):
    '''
    input() module loop with extended capabilities like type checking, 
    case sensitive check, choices list, custom rules, and more
    '''

    while True:
        usr = input(text)

        # type convert
        usr_converted = _change_type(usr, allow_type)
        if usr_converted is None:
            continue

        # rule validation
        if not _is_valid_rule(usr_converted, rule, rule_error):
            continue

        # string only checks
        if allow_type is str:
            if _string_checks(usr_converted, choices, case_sensitive):
                return usr_converted
            else:
                continue
        else:
            return usr_converted

def _string_checks(usr, choices, case_sensitive):
    if not choices:
        return True
    
    if not case_sensitive:
        usr = usr.lower()
        choices = [item.lower() for item in choices]

    if usr in choices:
        return True
    else:
        print(f'Invalid, please choose between ({", ".join(choices)})')
        return False

def _is_valid_rule(usr, rule, rule_error):
    try:
        valid_rule = rule(usr)
    except ValueError:
        print(rule_error)
        return False

    if not valid_rule:
        print(rule_error)
        return False

    return True

def _change_type(usr, allow_type):
    if allow_type is str:
        return usr
    try:
        return allow_type(usr)
    except (ValueError, TypeError):
        print(f'Invalid, {usr} is not a valid {allow_type.__name__}')
        return None
