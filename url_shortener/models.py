import re
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator
from django.db import models
from django.utils import timezone

URL_MAX_SHORT_ID_LEN = 12
# Maximum length for IE and several other search engines and protocols is
# 2047/2048.
URL_MAX_URL_LEN = 2047

class URL(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    # Set custom error message so it will never change with django updates.
    # This is a hack to be able to test on what ValidationError actually
    # occured.
    short_id_error = {
        'unique': 'Short id already used.'
    }
    short_id = models.CharField(
        max_length=URL_MAX_SHORT_ID_LEN,
        primary_key=True,
        validators=[alphanumeric]
    )
    url = models.URLField(max_length=URL_MAX_URL_LEN)
    added_date = models.DateTimeField('date added',
                                      default=timezone.now)

    # Overide save to automatically validate
    def save(self, *args, **kwargs):
        self.full_clean()
        super(URL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
