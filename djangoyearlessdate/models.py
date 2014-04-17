import datetime

from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

import forms
from helpers import value_is_MMDD_date


class YearlessDateField(models.CharField):
    "A model field for storing dates without years"
    description = "A date without a year, for use in things like birthdays"

    default_error_messages = {
        'invalid_date': _('Invalid date'),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4
        super(YearlessDateField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': forms.YearlessDateField}
        defaults.update(kwargs)
        return super(YearlessDateField, self).formfield(**defaults)

    def to_python(self, value):
        if value is None or value == '':
            return value

        if value_is_MMDD_date(value):
            return value
        else:
            raise exceptions.ValidationError(
                self.error_messages['invalid_date'],
                code='invalid',
            )


class YearField(models.IntegerField):
    "A model field for storing years, e.g. 2012"
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.YearField}
        defaults.update(kwargs)
        return super(YearField, self).formfield(**defaults)


#South integration
try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    #South is not installed
    pass
else:
    add_introspection_rules([], ["^djangoyearlessdate\.models\.YearlessDateField"])
    add_introspection_rules([], ["^djangoyearlessdate\.models\.YearField"])