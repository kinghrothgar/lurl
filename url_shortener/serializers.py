from rest_framework import serializers
from url_shortener.models import URL, URL_MAX_SHORT_ID_LEN, URL_MAX_URL_LEN

class URLSerializer(serializers.Serializer):
    short_id = serializers.CharField(max_length=URL_MAX_SHORT_ID_LEN)
    url = serializers.URLField(max_length=URL_MAX_URL_LEN)
    added_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return URL.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.short_id = validated_data.get('short_id', instance.short_id)
        instance.url = validated_data.get('url', instance.url)
        instance.added_date = validated_data.get('added_date', instance.added_date)

