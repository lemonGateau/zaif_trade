from math import ceil, floor


def round_up(value, ndigits=0):
    ''' ndigits: (組込み関数roundと同様)
        0のとき小数第1位,
        正のとき小数部  ,
        負のとき整数部    で切り上げ '''

    value *= 10**ndigits    # シフト
    value  = ceil(value)
    value *= 10**-ndigits   # シフト

    return value

def round_down(value, ndigits=0):
    ''' ndigits:(組み込み関数roundと同様) '''
    value *= 10** ndigits   # シフト
    value  = floor(value)
    value *= 10**-ndigits   # シフト

    return value
