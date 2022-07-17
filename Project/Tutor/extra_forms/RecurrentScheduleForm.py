from django import forms


from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class RecurrentScheduleForm(forms.Form):
    labels = {
        'start_day': 'Día de inicio',
        'end_day': 'Día de fin',
        'start_time': 'Hora de inicio',
        'end_time': 'Hora de fin',
    }
    widgets = {
        'start_day': DateTimePickerInput(
            format='%Y-%m-%d',
            attrs={'id': 'recurrent_start_day'},
            options={
                'locale': 'es'
            }
        ).start_of('day_block'),
        'end_day': DateTimePickerInput(
            format='%Y-%m-%d',
            attrs={'id': 'recurrent_end_day'},
            options={
                'locale': 'es'
            }
        ).end_of('day_block'),
        'start_time': DateTimePickerInput(
            format='%H:%M',
            attrs={'id': 'recurrent_start_time'},
            options={
                'locale': 'es',
                'stepping': '30'
            }
        ).start_of('time_block'),
        'end_time': DateTimePickerInput(
            format='%H:%M',
            attrs={'id': 'recurrent_end_time'},
            options={
                'locale': 'es',
                'stepping': '30'
            }
        ).end_of('time_block'),
    }

    start_day = forms.DateField(label=labels['start_day'], widget=widgets['start_day'])
    end_day = forms.DateField(label=labels['end_day'], widget=widgets['end_day'])
    start_time = forms.DateTimeField(label=labels['start_time'], widget=widgets['start_time'])
    end_time = forms.DateTimeField(label=labels['end_time'], widget=widgets['end_time'])

