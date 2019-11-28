def get_row(sheet, i, ch1, ch2):
    return sheet.range(f'{ch1}{i}:{ch2}{i}').value


def get_data1(a, b, c):
    global lands, lords, feods
    lands = a
    lords = b
    feods = c


def get_lands(feod):
    res = []
    for land in lands:
        if land.feod_name == feod.name:
            res.append(land)
    return res


def get_feod(feod_name):
    for feod in feods:
        if feod.name == feod_name:
            return feod


def get_feods(lord):
    res = []
    for feod in feods:
        if feod.owner_id == lord.id:
            res.append(feod)
    return res


def get_lord(id):
    for lord in lords:
        if lord.id == id:
            return lord