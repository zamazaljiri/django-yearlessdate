from django import forms
from django.forms.widgets import MultiWidget, TextInput
from django.core.validators import ValidationError
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from helpers import value_is_MMDD_date


class YearlessDateInput(TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'date-simple'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(YearlessDateInput, self).__init__(attrs=final_attrs)

    def _format_value(self, value):
        if value is None:
            return ''
        try:
            return '%02d.%02d.' % (int(value[2:]), int(value[:2]))
        except:
            return value

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value is None or len(value) == 0:
            return None
        list = value.split('.')
        if len(list) > 1:
            return '%s%s' % (list[1], list[0])
        return value


class YearlessDateField(forms.CharField):
    widget = YearlessDateInput

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(YearlessDateField, self).__init__(max_length=6, min_length=None, *args, **kwargs)
    
    def clean(self, value):
        if value is None or len(value) == 0:
            return super(YearlessDateField, self).clean(None)
        elif value_is_MMDD_date(value):
            return value
        else:
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
