def en_convert(number):
    files = {0: 'en_zero.WAV',
             1: 'en_1.WAV',
             2: 'en_2.WAV',
             3: 'en_3.WAV',    4: 'en_4.WAV',     5: 'en_5.WAV',
             6: 'en_6.WAV',      7: 'en_7.WAV',    8: 'en_8.WAV',
             9: 'en_9.WAV',     10: 'en_10.WAV', 11: 'en_11.WAV',
             12: 'en_12.WAV', 13: 'en_13.WAV',     14: 'en_14.WAV',
             15: 'en_15.WAV', 16: 'en_16.WAV',     17: 'en_17.WAV',
             18: 'en_18.WAV', 19: 'en_19.WAV',     20: 'en_20.WAV',
             30: 'en_30.WAV', 40: 'en_40.WAV',     50: 'en_50.WAV',
             60: 'en_60.WAV'}

    result_en = []
    if number <= 20:
        result_en.append(files[number])

    else:
        decimals, remainder = divmod(number, 10)
        if remainder != 0:
            result_en.append(files[decimals * 10])
            result_en.append(files[remainder])
        else:
            result_en.append(files[decimals * 10])

    return result_en
