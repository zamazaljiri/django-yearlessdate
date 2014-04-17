import calendar

from django import forms
from django.forms.widgets import MultiWidget, TextInput
from django.core.validators import ValidationError
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from helpers import YearlessDate


DAY_CHOICES =  tuple([('','---------' )] + [(i,i) for i in range(1,32)])
MONTH_CHOICES = tuple([('','---------' )] + [(i, calendar.month_name[i]) for i in range(1,13)])

    
class YearlessDateSelect(MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = (
            Select(attrs={'class': 'select-dateinyear-day'}, choices=DAY_CHOICES),
            Select(attrs={'class': 'select-dateinyear-month'}, choices=MONTH_CHOICES)
        )
        super(YearlessDateSelect, self).__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):
        if value is None:
            return [None,None]
        if not isinstance(value, YearlessDate):
            value = YearlessDate(value[2:], value[:2])
        return [value.day, value.month]


class YearlessDateInput(TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'date-simple'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(YearlessDateInput, self).__init__(attrs=final_attrs)

    def _format_value(self, value):
        if value is None:
            return ''
        if not isinstance(value, YearlessDate):
            if len(value) < 4:
                return ''
            value = YearlessDate(value[2:], value[:2])
        return '%02d.%02d.' % (value.day, value.month)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value is None or len(value) == 0:
            return ['', '']
        list = value.split('.')
        if len(list) > 1:
            return [list[0], list[1]]
        return value


class YearlessDateField(forms.Field):
    widget = YearlessDateInput
    
    def clean(self, value):
        if value == ['', '']:
            #If the values are both None, trigger the default validation for null
            super(YearlessDateField, self).clean(None)
        else:
            try:
                return YearlessDate(*value)
            except:
                raise ValidationError(_('Invalid date'))


class YearField(forms.Field):
    widget = TextInput
    
    def clean(self, value):
        #First, run general validation (will catch, for example, a blank entry
        #if the field is required
        super(YearField, self).clean(value)
        
        try:
            value = int(value)
            #TODO: allow customization of these limits
            if value < 1900 or value > 2200:
                raise Exception()
            return value
        except:
            raise ValidationError(_('Invalid year'))
