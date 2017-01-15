#-*- coding: utf-8 -*-

"""
@Author: SeonHo Lee (IT4211)
@E-mail: rhdqor100@live.co.kr
"""

vtag_list = ['rtf1', 'ansi', 'fcharset',
             'pard', 'par',
             'fldinstHYPERLINK', 'lang',
             'pict', 'picw', 'pich']

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
            print "[err]", e, "[_ch] ", _ch, "[stack] ", stack

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

        elif stack[-1] == 'U' and _ch.isalnum():
            seek +=1

        elif stack[-1] == 'U' and not _ch.isalnum():
            seek +=1
            stack.pop()

        elif stack[-1] == 'U' and _ch == '\\':
            stack.pop()
            stack.append('S')
            seek += 1

        elif stack[-1] == 'S' and _ch == '\\':
            seek += 1
            #print "[debug:stack:nop]", stack
            yield chunk, seek
            chunk = ""

        elif stack[-1] == 'S' and not _ch.isalnum():
            if _ch == '\'': # unicode data?
                stack.pop()
                stack.append('U') # state change
                chunk = ""
                seek += 1
                continue
            seek += 1
            yield chunk, seek
            stack.pop()
            #print "[debug:stack:pop]", stack

def tag_plain_list(tag_list, input):
    for tag, tag_offset, tag_data_offset, next_tag_offset in tag_list:
        if Valuable_tags(tag):  # 필요한 태그인가?
            if is_tag(tag_data_offset, input) == "tag": # 정보가 있는 태그인가?
                # 태그에서 숫자 값을 추 출 : 인코딩 정보 등 ...
                #print "[debug:info_tag:%s]" % (tag), input[tag_offset:next_tag_offset]
                pass

            elif is_tag(tag_data_offset, input) == "data": # 데이터 앞에 붙는 태그인가?
                # 다음 태그까지 데이터 읽어서 추출
                pict_of = is_pictag(tag, tag_offset)
                #print "[debug:pict_of]", pict_of
                if pict_of:
                    print "[debug:photo_tag:%s]" % tag, input[pict_of:tag_data_offset]
                    #print "[debug:photo_data]", input[tag_data_offset:next_tag_offset]
                else:
                    print tag, input[tag_data_offset:next_tag_offset-1]
        else:
            # 현재 유니코드를 not valuable 한 태그라고 인식함!
            #print "[debug:not valuable tag:%s]" % tag
            continue

def is_pictag(tag, tag_offset):
    if 'picw' in tag:
        return tag_offset + 4
    elif 'pich' in tag:
        return tag_offset + 4
    elif 'picwg' in tag:
        return tag_offset + 8
    elif 'pichg' in tag:
        return tag_offset + 8
    else:
        False

def Valuable_tags(tag):
    for vt in vtag_list:
        if vt in tag:
            return True
    return False

def is_tag(tag_data_offset, input):
    # 유니코드 오탐의 위험이 있음!
    if input[tag_data_offset] == None:
        return
    check_target = input[tag_data_offset-1]
    debug_target = input[tag_data_offset-1:tag_data_offset+20]
    try:
        if check_target == '\\':
            return "tag"
        elif check_target.isalnum():
            return "data"
        elif check_target == (' ' or '*' or '@'):
            is_tag(tag_data_offset+1, input)
        else:
            print "[err:istag][%s|%s]" % (check_target, debug_target)
    except AttributeError as e:
        print "[err]", e, "[data_off]", check_target, "[data]", debug_target

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
    tmp = str()
    tag_list = list()
    richtf = open("test2.rtf", "r")
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk

    tmp = tmp.replace('\\par', '\\par ')

    for tag, seek, in generator_taglist(tmp):
        tag_offset = seek - len(tag) - 1
        tag_data_offset = tag_offset + len(tag) #해당 태그 바로 뒤의 위치
        tag_set = [tag, tag_offset, tag_data_offset]
        #print "[TEST]", tag, tmp[tag_offset:tag_data_offset]
        tag_list.append(tag_set)

    tag_list = tag_list_handling(tag_list)

    for i in tag_list:
        print i

    tag_plain_list(tag_list, tmp)
    #for i in tag_plain_list(tag_list, tmp):
    #    print "[TEST]", i

    #print "[TEST]", tmp