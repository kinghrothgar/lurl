import re
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone

URL_MAX_SHORT_ID_LEN = 12
# Maximum length for IE and several other search engines and protocols is
# 2047/2048.
URL_MAX_URL_LEN = 2047

class URL(models.Model):
    short_id = models.CharField(max_length=URL_MAX_SHORT_ID_LEN, primary_key=True)
    url = models.URLField(max_length=URL_MAX_URL_LEN)
    added_date = models.DateTimeField('date added',
                                      default=timezone.now)

    def clean(self):
        # TODO: make max length and possible chars a setting or global variable
        if re.match('^[a-zA-Z0-9]{1,' + URL_MAX_SHORT_ID_LEN + '}$', self.short_id) is None:
            raise ValidationError({'short_id':
                'short_id must contain only a-zA-Z0-9 and max length of ' +
                                   URL_MAX_SHORT_ID_LEN
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super(URL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
