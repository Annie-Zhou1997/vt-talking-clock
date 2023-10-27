def en_convert(number):
    files = {0: 'en_zero.wav',
             1: 'en_1.wav',
             2: 'en_2.wav',
             3:  'en_3.wav',    4:  'en_4.wav',     5:  'en_5.wav',
             6:  'en_6.wav',      7:  'en_7.wav',    8:  'en_8.wav',
             9:  'en_9.wav',     10: 'en_10.wav'}

    # words = {'h': 'hour.wav',
    #          'm': 'minute.wav'}

    result_en = []
    if number <= 10:
        result_en.append(files[number])

    else:
        decimals, remainder = divmod(number, 10)
        if decimals > 1:
            if remainder != 0:
                result_en.append(files[decimals])
                result_en.append(files[10])
                result_en.append(files[remainder])
            else:
                result_en.append(files[decimals])
                result_en.append(files[10])
        else:
            result_en.append(files[10])
            if remainder != 0:
                result_en.append(files[remainder])



    return result_en