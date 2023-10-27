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
    elif number < 20:
        result_ch.append(files[10])
        result_ch.append(files[int(number)-10])
    else:
        result_ch.append(files[2])
        result_ch.append(files[10])
        result_ch.append(files[int(number)-20])

    return result_ch