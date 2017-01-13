"""
@Author: SeonHo Lee (IT4211)
@E-mail: rhdqor100@live.co.kr
"""

def bracket(input):
    # Brace removal function
    stack = list()
    chunk = str()
    rtftext = input.read()
    rtftext = rtftext.replace('\n', '')

    # simple pushdown automata
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

def generator_taglist(input):
    seek = 0
    stack = list()
    chunk = str()

    for _ch in input:
        if len(stack) == 0 and _ch == '\\':
            stack.append('S')
            #print "[debug:stack:push]", stack
            chunk = ""

        elif len(stack) == 0 and (_ch != '\\'):
            continue

        elif stack[-1] == 'S' and _ch.isalnum():
            chunk += _ch
            #print "[debug:chunk]", chunk
            seek += 1

        elif stack[-1] == 'S' and _ch == '\\':
            #print "[debug:stack:nop]", stack
            yield chunk
            chunk = ""

        elif stack[-1] == 'S' and not _ch.isalnum():
            yield chunk
            stack.pop()
            #print "[debug:stack:pop]", stack

if __name__=="__main__":
    tmp = str()
    tag_list = list()
    richtf = open('test.rtf', 'r')
    plaintf = open('rtf2pt.txt', 'w')
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk
        tmp = tmp.replace("\\rtlch", "\n\\rtlch")

    for i in generator_taglist(tmp):
        if i != "":
            tag_list.append(i)
            print i

