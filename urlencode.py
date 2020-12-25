# Credit:
# https://github.com/lucien2k/wipy-urllib/blob/ad151bb3838d464e86ce6453f5cdc29675bc0f27/urequests.py#L155

always_safe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-'

def quote(s):
    res = []
    for c in s:
        if c in always_safe:
            res.append(c)
            continue
        res.append('%%%x' % ord(c))
    return ''.join(res)

def urlencode(query):
    if isinstance(query, dict):
        query = query.items()
    l = []
    for k, v in query:
        if not isinstance(v, list):
            v = [v]
        for value in v:
            k = quote(str(k))
            v = quote(str(value))
            l.append(k + '=' + v)
    return '&'.join(l)
