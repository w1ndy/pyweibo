NUMERIC_MAP = {
    '\u5341': 10,
    '\u767e': 100,
    '\u5343': 1000,
    '\u4e07': 10000,
    '\u4ebf': 100000000
}

def parseChineseNumeric(s):
    base = 1
    while len(s):
        if s[-1] in NUMERIC_MAP:
            base *= NUMERIC_MAP[s[-1]]
            s = s[:-1]
        else:
            return base * float(s)
    return base
