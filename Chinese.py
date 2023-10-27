def ch_convert(number):
    files = {0: 'zero.wav',
             1: 'one.wav',
             2: 'two.wav',
             3:  'three.wav',    4:  'four.wav',     5:  'five.wav',
             6:  'six.wav',      7:  'seven.wav',    8:  'eight.wav',
             9:  'nine.wav',     10: 'ten.wav'}

    # words = {'h': 'hour.wav',
    #          'm': 'minute.wav'}

    result_ch = []
    if number <= 10:
        result_ch.append(files[number])

    else:
        decimals, remainder = divmod(number, 10)
        if decimals > 1:
            if remainder != 0:
                result_ch.append(files[decimals])
                result_ch.append(files[10])
                result_ch.append(files[remainder])
            else:
                result_ch.append(files[decimals])
                result_ch.append(files[10])
        else:
            result_ch.append(files[10])
            if remainder != 0:
                result_ch.append(files[remainder])



    return result_ch