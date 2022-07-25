from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
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
    if visit_minutes < minutes:
        return False
    else:
        return True


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits_by_passcard = get_list_or_404(Visit, passcard=passcard)

    this_passcard_visits = []

    for visit in visits_by_passcard:
        duration = format_duration(get_duration(visit))
        long_visit_flag = is_visit_long(visit)
        filled_template = {
            'entered_at': visit.entered_at,
            'duration': duration,
            'is_strange': long_visit_flag
        }
        this_passcard_visits.append(filled_template)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
