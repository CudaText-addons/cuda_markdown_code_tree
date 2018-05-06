def _is_pre(s, ch):
    if not s.startswith(ch):
        return
    r = 0
    for i in range(min(10, len(s))):
        if s[i] == ch:
            r += 1
        else:
            break
    return r


def is_line_ticks(s):
    return _is_pre(s, '`')


def is_line_head(s):
    return _is_pre(s, '#')


def gen_markdown_headers(lines):
    '''
    Generates markdown headers in format:
    line_number, header_level, header_text
    '''
    res = []
    tick = False
    tick_r = 0
    for i, s in enumerate(lines):
        if not s.strip():
            continue
        r = is_line_ticks(s)
        if r:
            if tick and r == tick_r:
                tick = False
                tick_r = 0
            else:
                tick = True
                tick_r = r
            continue
        if tick:
            continue
        r = is_line_head(s)
        if r:
            yield i, r - 1, s[r:].strip()
    return res
