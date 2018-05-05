
CHAR_TICK = '`' # this char, in any repeat count, means start/end of code block

def is_line_ticks(s):
    if not s.startswith(CHAR_TICK): return
    r = 0
    for i in range(min(10, len(s))):
        if s[i]==CHAR_TICK:
            r += 1
        else:
            break
    return r
         
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
    (line_index, level_from_1, line_text_after#)
    '''
    
    res = []
    tick = False
    tick_r = 0

    for (i, s) in enumerate(lines):
        if not s.strip(): continue
        
        r = is_line_ticks(s)
        if r:
            if tick and r==tick_r:
                tick = False
                tick_r = 0
            else:
                tick = True
                tick_r = r
            continue
            
        if tick: continue
        r = is_line_head(s)
        if r:
            res += [(i, r, s[r:])]
    
    return res
