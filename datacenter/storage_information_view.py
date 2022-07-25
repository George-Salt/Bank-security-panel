from datacenter.models import Visit
from django.shortcuts import get_list_or_404
from django.shortcuts import render
from django.utils.timezone import localtime


def get_duration(visit):
    time_now = localtime()
    delta = time_now - visit.entered_at
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


def storage_information_view(request):
    non_closed_visits_info = get_list_or_404(Visit, leaved_at=None)

    non_closed_visits = []
    for visit in non_closed_visits_info:
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        owner_name = visit.passcard.owner_name
        entry_time = localtime(visit.entered_at)
        long_visit_flag = is_visit_long(visit)

        filled_template = {
            'who_entered': owner_name,
            'entered_at': entry_time,
            'duration': formatted_duration,
            'is_strange': long_visit_flag
        }
        non_closed_visits.append(filled_template)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
