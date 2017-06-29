from rest_framework import serializers
from url_shortener.models import URL, URL_MAX_SHORT_ID_LEN

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('short_id', 'url', 'added_date')
        read_only_fields = ('added_date',)
        extra_kwargs = {
            'short_id' : {'read_only' : True}
        }
