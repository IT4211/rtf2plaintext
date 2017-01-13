#-*- coding: utf-8 -*-
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
            seek += 1
            stack.append('S')
            #print "[debug:stack:push]", stack
            chunk = ""

        elif len(stack) == 0 and (_ch != '\\'):
            seek += 1
            continue

        elif stack[-1] == 'S' and _ch.isalnum():
            chunk += _ch
            #print "[debug:chunk]", chunk
            seek += 1

        elif stack[-1] == 'S' and _ch == '\\':
            seek += 1
            #print "[debug:stack:nop]", stack
            yield chunk, seek
            chunk = ""

        elif stack[-1] == 'S' and not _ch.isalnum():
            seek += 1
            yield chunk, seek
            stack.pop()
            #print "[debug:stack:pop]", stack

if __name__=="__main__":
    tmp = str()
    tag_list = list()
    richtf = open('test.rtf', 'r')
    plaintf = open('rtf2pt.txt', 'w')
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk

    for tag, seek in generator_taglist(tmp):
        tag_offset = seek - len(tag) - 1
        tag_data_offset = tag_offset + len(tag) #해당 태그 바로 뒤의 위치
        print "[TEST]", tag, tmp[tag_offset:tag_data_offset]

