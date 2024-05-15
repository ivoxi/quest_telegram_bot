import os


def check_condition_desc(user, text, *conditions, logical_operator="AND"):
    result = []
    for condition in conditions:
        part, key, symbol, value = condition
        current_value = getattr(user, part).get(key)
        if symbol == "=":
            if current_value == value:
                result.append(True)
            else:
                result.append(False)
        elif symbol == ">":
            if current_value > value:
                result.append(True)
            else:
                result.append(False)
        elif symbol == "<":
            if current_value < value:
                result.append(True)
            else:
                result.append(False)
        elif symbol == "exist":
            if current_value == value:
                result.append(False)
            else:
                result.append(True)
            break
    if logical_operator == "AND":
        if all(result):
            return text
    elif logical_operator == "OR":
        if any(result):
            return text
    return ""


def check_file_in_directory(directory, filename):
    files_in_directory = os.listdir(directory)
    if filename in files_in_directory:
        return True
    else:
        return False
