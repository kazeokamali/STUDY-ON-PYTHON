import random
import string

ALL_code = string.digits + string.ascii_letters

def code_make(*,l = 6):
    verify_code = ''.join( random.choices( ALL_code, k = l ))
    return verify_code

print(code_make(l = 4))
