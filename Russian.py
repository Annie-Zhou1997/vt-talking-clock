def ru_convert(number, mode):
    files = {0: 'zero.wav',
             1: {'h': 'one_masc.wav', 'm': 'one_fem.wav'},
             2: {'h': 'two_masc.wav', 'm': 'two_fem.wav'},
             3:  'three.wav',    4:  'four.wav',     5:  'five.wav',
             6:  'six.wav',      7:  'seven.wav',    8:  'eight.wav',
             9:  'nine.wav',     10: 'ten.wav',      11: 'eleven.wav',
             12: 'twelve.wav',   13: 'thirteen.wav', 14: 'fourteen.wav',
             15: 'fifteen.wav',  16: 'sixteen.wav',  17: 'seventeen.wav',
             18: 'eighteen.wav', 19: 'nineteen.wav', 20: 'twenty.wav',
             30: 'thirty.wav',   40: 'forty.wav',    50: 'fifty.wav'}

    words = {'h': {'pl': 'hrs_pl.wav', 'nom': 'hrs_nom.wav', 'cf': 'hrs_cf.wav'},
             'm': {'pl': 'min_pl.wav', 'nom': 'min_nom.wav', 'cf': 'min_cf.wav'}}

    result = []
    if number == 0:
        result.append(files[0])
        result.append(words[mode]['pl'])
    else:
        decimals, remainder = divmod(number, 10)
        if decimals > 1:
            result.append(files[decimals * 10])
            number = remainder
        if number == 0:
            result.append(words[mode]['pl'])
        elif number == 1:
            result.append(files[number][mode])
            result.append(words[mode]['nom'])
        elif number == 2:
            result.append(files[number][mode])
            result.append(words[mode]['cf'])
        elif number in (3, 4):
            result.append(files[number])
            result.append(words[mode]['cf'])
        else:
            result.append(files[number])
            result.append(words[mode]['pl'])

    return result