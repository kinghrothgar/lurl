import logging, random, re, string
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from url_shortener.models import URL, URL_MAX_SHORT_ID_LEN
from url_shortener.serializers import URLSerializer

SHORT_ID_LEN = 6

logger = logging.getLogger(__name__)

class URLDetails(APIView):
    def get_url(self, short_id):
        if re.match('^[a-zA-Z0-9]{1,' + str(URL_MAX_SHORT_ID_LEN) + '}$', short_id) is None:
            raise Http404

        try:
            return URL.objects.get(short_id=short_id)
        except URL.DoesNotExist:
            raise Http404

    def get(self, request, short_id, format=None):
        url = self.get_url(short_id)
        serializer = URLSerializer(url)
        return Response(serializer.data)

    def delete(self, request, short_id, format=None):
        url = self.get_url(short_id)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class URLNew(APIView):
    def post(self, request, format=None):
        serializer = URLSerializer(data=request.data)
        # If it fails to  validate, that means the given URL wasn't valid
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        tries = 0
        stored = False
        chars = string.ascii_letters + string.digits
        while not stored:
            # Don't want to get stuck in a infinite loop slamming the DB
            # If it takes more than 3 tries, there are not enough short_ids
            # left of length SHORT_ID_LEN or something else is very wrong
            if tries >= 3:
                logger.error('ERROR: 3 failed attempts to find unused short_id')
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            ran_str = ''
            for _ in range(SHORT_ID_LEN):
                ran_str += random.SystemRandom().choice(chars)

            try:
                tries += 1
                serializer.save(short_id=ran_str)
                stored = True
            except ValidationError as e:
                errors = e.message_dict
                if ('short_id' in errors and
                    errors['short_id'] == 'Short id already used.'):
                    # If this is true, try loop again to try another short_id
                    pass
                else:
                    logger.error('ERROR: Uncaught validation error: ' + str(e))
                    return Response(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        if tries > 1:
            logger.warn(
                'WARN: encountered {} short_id collisions'.format(tries)
            )
        return Response(serializer.data)
