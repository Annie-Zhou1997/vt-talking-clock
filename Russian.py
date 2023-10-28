def ru_convert(time):
    hours, mins = (int(x) for x in time.split(':'))
    hours_pm = hours - 12 if hours >= 12 else hours

    files = {0: {'nom': 'zero.wav'},
             1: {'h': 'one_masc.wav', 'm': 'one_fem.wav', 'nom': 'hrs_nom.wav', 'adj_gen': 'one_adj_gen.wav'},
             2: {'h': 'two_masc.wav', 'm': 'two_fem.wav', 'nom': 'two_masc.wav', 'adj_gen': 'two_adj_gen.wav'},
             3: {'nom': 'three.wav', 'adj_gen': 'three_adj_gen.wav'},
             4: {'nom': 'four.wav', 'adj_gen': 'four_adj_gen.wav'},
             5: {'nom': 'five.wav', 'adj_gen': 'five_adj_gen.wav', 'num_gen': 'five_num_gen.wav'},
             6: {'nom': 'six.wav', 'adj_gen': 'six_adj_gen.wav'},
             7: {'nom': 'seven.wav', 'adj_gen': 'seven_adj_gen.wav'},
             8: {'nom': 'eight.wav', 'adj_gen': 'eight_adj_gen.wav'},
             9: {'nom': 'nine.wav', 'adj_gen': 'nine_adj_gen.wav'},
             10: {'nom': 'ten.wav', 'adj_gen': 'ten_adj_gen.wav', 'num_gen': 'ten_num_gen.wav'},
             11: {'nom': 'eleven.wav', 'adj_gen': 'eleven_adj_gen.wav'},
             12: {'nom': 'twelve.wav', 'adj_gen': 'twelve_adj_gen.wav'},
             13: {'nom': 'thirteen.wav'},
             14: {'nom': 'fourteen.wav'},
             15: {'nom': 'fifteen.wav', 'num_gen': 'fifteen_num_gen.wav'},
             16: {'nom': 'sixteen.wav'},
             17: {'nom': 'seventeen.wav'},
             18: {'nom': 'eighteen.wav'},
             19: {'nom': 'nineteen.wav'},
             20: {'nom': 'twenty.wav', 'num_gen': 'twenty_num_gen.wav'},
             30: {'nom': 'thirty.wav'},
             40: {'nom': 'forty.wav'},
             50: {'nom': 'fifty.wav'}}

    words = {'h': {'pl': 'hrs_pl.wav', 'nom': 'hrs_nom.wav', 'cf': 'hrs_cf.wav'},
             'm': {'pl': 'min_pl.wav', 'nom': 'min_nom.wav', 'cf': 'min_cf.wav'},
             'half': 'half.wav',
             'without': 'without.wav'}

    result = []
    if mins == 30:  # half h+1.adj.gen
        result.extend([words['half'], files[hours_pm+1]['adj_gen']])
    elif mins in (5, 10, 15, 20):  # n.nom min.gen.pl hour+1.adj.gen
        result.extend([files[mins]['nom'], words['m']['pl'], files[hours_pm+1]['adj_gen']])
    elif mins in (40, 45, 50, 55):  # without 60-min.num.gen hour+1.nom
        result.extend([words['without'], files[60-mins]['num_gen'], files[hours_pm+1]['nom']])
    else:
        for mode, number in {'h': hours, 'm': mins}.items():
            if number == 0:
                result.append(files[0])
                result.append(words[mode]['pl'])
            else:
                decimals, remainder = divmod(number, 10)
                if decimals > 1:
                    result.append(files[decimals * 10]['nom'])
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
                    result.append(files[number]['nom'])
                    result.append(words[mode]['cf'])
                else:
                    result.append(files[number]['nom'])
                    result.append(words[mode]['pl'])

    return result
