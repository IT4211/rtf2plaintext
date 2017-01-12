"""
@Author: SeonHo Lee (IT4211)
@E-mail: rhdqor100@live.co.kr
"""
def rtf2plaintext(thefile):
    f = open(thefile, 'r')
    ptxt = open('plaintext.txt', 'w')
    parse(f)
    #TODO : ptxt.write(parsing(rtf))
    f.close()
    ptxt.close()

def parse(input):

    stack = list()
    txtag = ['loch', 'hich', 'dbch']

    while True:
        next = input.read(1)

        if not next:
            break

        if next == '{':
            stack.append('G')
            print "[debug:stack]", stack

        elif next == '}' and stack[-1] == 'G':
            stack.pop()
            print "[debug:stack]", stack

        elif next == '\\' and stack[-1] == 'G':
            tag = input.read(5)
            print "[debug:tag]", tag
            if tag == 'rtlch':
                stack.append('T')
                print "[debug:stack]", stack

            elif stack[-1] == 'T' and check_tag(tag, txtag):
                stack.pop()
                stack.append('R')
                print "[debug:stack]", stack

            elif stack[-1] == 'R' and check_pt(tag, "ch\f"):
                stack.pop()
                stack.append('PT')
                print "[debug:stack]", stack

                if stack[-1] == 'PT':
                    while input.read(1) == ' ':
                        break
                    pt_of = input.tell()
                    print "[debug:plain text offset]", pt_of

        else:
            continue

def check_tag(tag, txtag):
    for tx in txtag:
        if tag in tx:
            return True
    return False

def check_pt(tag, pttag):
    if tag in pttag:
        return True
    return True


if __name__=="__main__":
    rtf2plaintext("test.rtf")