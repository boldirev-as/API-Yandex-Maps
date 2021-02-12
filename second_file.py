def get_size_toponym(toponym, static=True):
    if static:
        toponym_upper_lower = toponym["boundedBy"]["Envelope"]
        toponym_upper, toponym_lower = toponym_upper_lower["lowerCorner"].split(" ")
        toponym_upper_2, toponym_lower_2 = toponym_upper_lower["upperCorner"].split(" ")
    else:
        pass

    delta_1 = round(abs(float(toponym_lower) - float(toponym_lower_2)) / 2, 6)
    delta_2 = round(abs(float(toponym_upper) - float(toponym_upper_2)) / 2, 6)
    return delta_1, delta_2
