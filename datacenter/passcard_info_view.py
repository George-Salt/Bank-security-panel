from datacenter.models import Passcard, Visit
from datacenter.session_processing_tools import get_duration, format_duration, is_visit_long
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import render


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
