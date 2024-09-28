from datetime import timedelta


def ms_to_hmsms(ms):
    td = timedelta(milliseconds=ms)
    h, remainder = divmod(td.seconds, 3600)
    m, s = divmod(remainder, 60)
    ms = td.microseconds // 1000
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"
