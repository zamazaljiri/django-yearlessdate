import datetime

def value_is_MMDD_date(value):
    if value is None or value == '':
        return True
    if len(value) == 4:
        try:
            datetime.date(year=2008, month=int(value[:2]), day=int(value[2:]))
            return True
        except ValueError:
            return False
    return False
