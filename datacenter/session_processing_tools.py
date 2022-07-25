from django.utils.timezone import localtime


def get_duration(visit):
    if not visit.leaved_at:
        time_now = localtime()
        delta = time_now - visit.entered_at
    else:
        delta = visit.leaved_at - visit.entered_at
    return delta


def format_duration(duration):
    seconds = duration.total_seconds()
    hours = int(seconds / 3600)
    minutes = int(((seconds % 3600) / 60) - (hours / 60))
    if minutes < 10:
        return f'{hours}:0{minutes}'
    else:
        return f'{hours}:{minutes}'


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    visit_minutes = duration.total_seconds() / 60
    return visit_minutes < minutes
