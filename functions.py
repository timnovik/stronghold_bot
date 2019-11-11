def get_row(sheet, i, ch1, ch2):
    return sheet.range(f'{ch1}{i}:{ch2}{i}').value

def get_lands(lord, lands):
    res = []
    for land in lands:
        if land.owner_id == lord.id:
            res.append(land)
    return res


def get_lord(id, lords):
    for lord in lords:
        if lord.id == id:
            return lord