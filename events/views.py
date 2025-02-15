from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Event, EventRegistration
from .forms import EventRegistrationForm

def event_list(request):
    upcoming_events = Event.objects.filter(
        end_datetime__gte=timezone.now()
    ).order_by('start_datetime')
    
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'events/event_list.html', context)

def event_calendar(request):
    return render(request, 'events/event_calendar.html')

def get_events_json(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = Event.objects.filter(
        start_datetime__gte=start,
        end_datetime__lte=end
    )
    
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_datetime.isoformat(),
            'end': event.end_datetime.isoformat(),
            'url': f'/events/{event.id}/',
            'className': f'event-type-{event.event_type}'
        })
    
    return JsonResponse(event_list, safe=False)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registration = None
    registration_form = None

    if request.user.is_authenticated:
        user_registration = EventRegistration.objects.filter(
            event=event,
            user=request.user
        ).first()

        if event.is_registration_open() and not user_registration:
            registration_form = EventRegistrationForm()

    context = {
        'event': event,
        'user_registration': user_registration,
        'registration_form': registration_form,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not event.is_registration_open():
        messages.error(request, 'Registration is closed for this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, 'Successfully registered for the event!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventRegistrationForm()
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/event_register.html', context)

@login_required
def cancel_registration(request, pk):
    registration = get_object_or_404(EventRegistration, 
        event_id=pk, 
        user=request.user
    )
    
    if request.method == 'POST':
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, 'Event registration cancelled successfully.')
        return redirect('event_detail', pk=pk)
    
    return render(request, 'events/cancel_registration.html', {
        'registration': registration
    }) 