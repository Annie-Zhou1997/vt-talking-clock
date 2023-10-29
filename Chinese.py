def ch_convert(number):
    files = {0: 'zero.wav', 1: 'one.wav', 2: 'two.wav',
             3: 'three.wav', 4: 'four.wav', 5: 'five.wav',
             6: 'six.wav', 7: 'seven.wav', 8: 'eight.wav',
             9: 'nine.wav', 10: 'ten.wav'}

    result = []
    if number <= 10:
        result.append(files[number])
    else:
        decimals, remainder = divmod(number, 10)
        if decimals > 1:
            if remainder != 0:
                result.append(files[decimals])
                result.append(files[10])
                result.append(files[remainder])
            else:
                result.append(files[decimals])
                result.append(files[10])
        else:
            result.append(files[10])
            if remainder != 0:
                result.append(files[remainder])

    return result