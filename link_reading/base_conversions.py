def baseconvert(n, base):
    """convert positive decimal integer n to equivalent in another base (2-36)"""

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"

    try:
        n = int(n)
        base = int(base)
    except:
        return ""

    if n < 0 or base < 2 or base > 36:
        return ""

    s = ""

    while 1:
        r = n % base
        s = digits[r] + s
        n -= r
        n = int(n / base)
        if n == 0:
            break

    return s