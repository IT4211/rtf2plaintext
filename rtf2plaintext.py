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


def parse_plaintext(input):
    chk_pt_tag = ['sectd', 'pard', 'plain', 'rtlch']
    seek = 0
    stack = list()
    chunk = str()
    pt_offset = str()

    for _ch in input:
        if len(stack) == 0 and _ch == '\\':
            stack.append('S')

        elif stack[-1] == 'S' and _ch.isalpha():
            chunk += _ch
            seek += 1

        elif stack[-1] == 'S' and (_ch == '\\' or not _ch.isalpha()):
            stack.pop()
            if len(stack) == 0:
                if chk_pt_tag[0] in chunk:
                    continue
                elif chk_pt_tag[1] in chunk:
                    continue
                elif chk_pt_tag[2] in chunk:
                    continue
                elif chk_pt_tag[3] in chunk:
                    pt_offset = input[seek:]
                    break

    for _ch in pt_offset:
        print "[d]", _ch







if __name__=="__main__":
    tmp = str()
    richtf = open('test.rtf', 'r')
    plaintf = open('rtf2pt.txt', 'w')
    for tag_chunk in bracket(richtf):
        tmp += tag_chunk
        tmp = tmp.replace("\\rtlch", "\n\\rtlch")
       #plaintf.write(tmp)
        parse_plaintext(tmp)


    #print file_meta_tag(tmp)
