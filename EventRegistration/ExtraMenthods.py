
def remove_char(s, i):
    b = bytearray(s, 'utf-8')
    del b[i]
    return b.decode()