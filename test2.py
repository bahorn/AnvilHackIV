import re
def get_current_word(line, position):
    try:
        first = re.findall(r"[\w]+",line[:position])
        second = re.findall(r"[\w]+",line[position:])
        if first == []: first = line[:position]
        if second == []: second = line[postion:]
        return first[-1]+second[0]
    except:
        return ""
if __name__ == "__main__":
    print get_current_word("(hello world)", 7)
    print get_current_word("(hello world)", 2)
    print get_current_word("(hello world)", 9)
