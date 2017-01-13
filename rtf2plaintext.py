#-*- coding: utf-8 -*-

"""
@Author: SeonHo Lee (IT4211)
@E-mail: rhdqor100@live.co.kr
"""

vtag_list = ['rtf1', 'ansi', 'fcharset', 'generator', 'pard', 'par']

def bracket(input):
    # Brace removal function
    stack = list()
    chunk = str()
    rtftext = input.read()
    rtftext = rtftext.replace('\n', '')

    # simple pushdown automata
    for _ch in rtftext:
        if _ch == '\0': #wordpad .rtf 일 경우, 마지막 NULL 처리!
            return
        try:
            if len(stack) == 0 and _ch == '{':
                stack.append('G')
                #print "[debug:stack:push]", stack

            elif stack[-1] == 'G' and _ch == '{':
                stack.append('G')
                #print "[debug:stack:push]", stack

            elif stack[-1] == 'G' and _ch != '}':
                chunk += _ch

            elif stack[-1] == 'G' and _ch == '}':
                stack.pop()
                #print "[debug:stack:pop]", stack
                if len(stack) == 0:
                    #print "[debug:chunk]", chunk
                    yield chunk

        except IndexError as e:
            print "[error]", e, "[_ch] ", _ch, "[stack] ", stack

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

def tag_plain_list(tag_list, input):
    for tag, tag_offset, tag_data_offset, next_tag_offset in tag_list:
        if Valuable_tags(tag):  # 필요한 태그인가?
            if is_tag(tag_data_offset, input) == "tag": # 정보가 있는 태그인가?
                # 태그에서 숫자 값을 추출
                print "[debug:info_teg]"
                pass
            elif is_tag(tag_data_offset, input) == "data": # 데이터 앞에 붙는 태그인가?
                # 다음 태그까지 데이터 읽어서 추출
                #raw_data.append(input[tag_data_offset:next_tag_offset])
                #yield raw_data
                print input[tag_data_offset:next_tag_offset]
        else:
            continue

def Valuable_tags(tag):
    #vtag_list = ['rtf1', 'ansi', 'fcharset', 'pard', 'par']
    if tag in vtag_list:
        return True
    else:
        return False

def is_tag(tag_data_offset, input):
    # 유니코드 오탐의 위험이 있음!
    check_target = input[tag_data_offset+1]
    debug_target = input[tag_data_offset+1:tag_data_offset+10]
    try:
        if check_target == '\\':
            return "tag"
        elif check_target.isalnum():
            return "data"
        elif check_target == ' ':
            is_tag(tag_data_offset+1, input)
        else:
            print "[err:istag] |%s|%s|" % (check_target, debug_target)
    except AttributeError as e:
        print "[err]", e, "[data_off]", check_target, "data", debug_target

def tag_list_handling(tag_list):
    offset_list = []
    for tag, offset, data_offset in tag_list:
        offset_list.append(offset)

    last_tag_offset = offset_list[-1]
    offset_list = offset_list[1:]
    offset_list.append(last_tag_offset)

    for i, offset in enumerate(offset_list):
        tag_list[i].append(offset_list[i])

    return tag_list


if __name__=="__main__":
    """
    tmp = str()
    tag_list = list()
    richtf = open('test.rtf', 'r')
    plaintf = open('rtf2pt.txt', 'w')
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk

    for tag, seek in generator_taglist(tmp):
        tag_offset = seek - len(tag) - 1
        tag_data_offset = tag_offset + len(tag) #해당 태그 바로 뒤의 위치
        tag_set = [tag, tag_offset, tag_data_offset]
        #print "[TEST]", tag, tmp[tag_offset:tag_data_offset]
        tag_list.append(tag_set)

    for i in tag_list:
        print i
    """
    tmp = str()
    tag_list = list()
    richtf = open("test2.rtf", "r")
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk
        #tmp += tag_chunk

    tmp = tmp.replace('\\par', '\\par ')

    for tag, seek, in generator_taglist(tmp):
        tag_offset = seek - len(tag) - 1
        tag_data_offset = tag_offset + len(tag) #해당 태그 바로 뒤의 위치
        tag_set = [tag, tag_offset, tag_data_offset]
        #print "[TEST]", tag, tmp[tag_offset:tag_data_offset]
        tag_list.append(tag_set)

    tag_list = tag_list_handling(tag_list)

    #for i in tag_list:
    #    print i

    tag_plain_list(tag_list, tmp)
    #for i in tag_plain_list(tag_list, tmp):
    #    print "[TEST]", i

    #print "[TEST]", tmp