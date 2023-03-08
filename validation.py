import re


def validate_checks(vals):
    res = 0
    for i in vals:
        res += int(i)
    if res == 0:
        # print("invalid")
        raise ValueError("No algorithms chosen!")
    # print("valid")


def validate_code(string, code_list):
    if not len(string):
        raise ValueError("Enter code!")
    for code in string.split():
        if len(code) > 5:
            raise ValueError("Each code cannot be longer than 5 characters!")
        if not re.match('[-\*\·\.\•\_\—\–\/]+$', code):
            raise ValueError("Illegal character used!")
        code, n = re.subn('[\*\·\.]', '•', code)
        code, n = re.subn('[-\_\—\–]', '–', code)
        if not code in code_list and code !="/":
            raise ValueError(f'Code {code} is not supported by this Morse table!')


def validate_text(text):
    if not len(text):
        raise ValueError("Enter text!")
    if not re.match('[a-zA-Z0-9\s]+$', text):
        raise ValueError("Input may contain only numbers, spaces and latin letters!")


