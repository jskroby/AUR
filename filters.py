def float_filter(integer):
    return float(integer)


def timestamp_filter(timestamp):
    import datetime
    from dateutil.tz import tzutc
    t = datetime.datetime.fromtimestamp(int(timestamp) / 1000, tz=tzutc())
    return t.strftime('%d.%m.%y %H:%M:%S')
