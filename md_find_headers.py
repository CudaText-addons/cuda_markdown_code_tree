
CHAR_TICK = '`' # this char, in any repeat count, means start/end of code block

def is_line_ticks(s):
    if not s: return False
    for ch in s:
        if ch!=CHAR_TICK: return False
    return True
     
def is_line_head(s):
    if not s.startswith('#'): return
    r = 0
    for i in range(min(10, len(s))):
        if s[i]=='#':
            r += 1
        else:
            break
    return r
        

def markdown_find_headers(lines):
    '''
    Gets list of headers, each list item is tuple
    (line_index, line_text, int_header_level_from_1)
    '''
    
    res = []
    tick = False
    tick_s = ''

    for (i, s) in enumerate(lines):
        if not s.strip(): continue
        
        if is_line_ticks(s):
            if tick and s==tick_s:
                tick = False
                tick_s = ''
            else:
                tick = True
                tick_s = s
            continue
            
        if tick: continue
        r = is_line_head(s)
        if r:
            res += [(i, s, r)]
    
    return res
