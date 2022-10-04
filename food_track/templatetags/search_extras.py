from django import template

register = template.Library()

@register.filter(name='process_qry')
def process_qry(value):
    res = ""
    i = 0
    while i < len(value):
        if value[i] == '&':
            return res
        elif value[i] == '+':
            res += " "
        elif value[i] == '%':
            punctuation = value[i:i+3]
            if punctuation == '%20':
                res += " "
            elif punctuation == '%27':
                res += "'"
            elif punctuation == '%21':
                res += "!"
            elif punctuation == '%26':
                res += "&"
            elif punctuation == "%3A":
                res += ":"
            else:
                i += 1
                continue
            i += 3
            continue
        else:
            res += value[i]
        i += 1
    return res