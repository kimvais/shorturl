import string
CHARSET=string.digits+string.ascii_letters+"$-_.+!*" 
BASE=len(CHARSET)
L = 4

def itou(i):
    digits = tobase(BASE,i)
    u = [CHARSET[int(x)] for x in digits]
    return "".join(u)

def utoi(u):
    u= list(u)
    u.reverse()
    i = 0
    for pos in range(0,len(u)):
        i += BASE**pos*CHARSET.find(u[pos]) 
    return i

def tobase(base,number):
    global tb
    def tb(b,n,result=[]):
        if n == 0: return result
        else: return tb(b,n/b,[str(n%b)]+result)

    if not isinstance(base, int):
        raise TypeError, 'invalid base for tobase()'
    if base <= 0:
        raise ValueError, 'invalid base for tobase(): %s' % base
    if (not isinstance(number,int)) and (not isinstance(number, long)):
        raise TypeError, 'tobase() of non-integer'
    if number == 0:
        return '0'
    if number > 0:
        return tb(base, number)
    if number < 0:
        return '-' + tb(base, -1*number)

