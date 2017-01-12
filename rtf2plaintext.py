"""
@Author: SeonHo Lee (IT4211)
@E-mail: rhdqor100@live.co.kr
"""

def bracket(input):
    #
    stack = list()
    chunk = str()
    rtftext = input.read()

    for _ch in rtftext:
        if len(stack) == 0 and _ch == '{':
            stack.append('G')

        elif stack[-1] == 'G' and _ch == '{':
            stack.append('G')

        elif stack[-1] == 'G' and _ch != '}':
            chunk += _ch

        elif stack[-1] == 'G' and _ch == '}':
            stack.pop()
            if len(stack) == 0:
                yield chunk


if __name__=="__main__":
    richtf = open('test.rtf', 'r')
    for tag_chunk in bracket(richtf):
        print tag_chunk
