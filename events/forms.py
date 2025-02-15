from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['num_guests', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_num_guests(self):
        num_guests = self.cleaned_data['num_guests']
        event = self.instance.event
        total_participants = event.get_registered_count() + num_guests + 1  # +1 for the registrant

        if event.max_participants and total_participants > event.max_participants:
            remaining_spots = event.max_participants - event.get_registered_count()
            raise forms.ValidationError(
                f'Only {remaining_spots} spots remaining. Cannot register {num_guests + 1} participants.'
            )
        return num_guests 