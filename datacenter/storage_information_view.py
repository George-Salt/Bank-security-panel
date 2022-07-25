from datacenter.models import Visit
from datacenter.session_processing_tools import get_duration, format_duration, is_visit_long
from django.shortcuts import get_list_or_404
from django.shortcuts import render
from django.utils.timezone import localtime


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
