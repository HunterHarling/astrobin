from django.template.loader import render_to_string
from django.conf import settings
from django.utils import translation

import urllib2
import simplejson
from notification import models as notification

def push_notification(recipients, type, data):
    data['notices_url'] = settings.ASTROBIN_BASE_URL + '/notifications/'
    data['LANGUAGE_CODE'] = translation.get_language()
    try:
        notification.send(recipients, type, data)
    except:
        pass


    if settings.LONGPOLL_ENABLED:
        rendered = render_to_string('notification/%s/%s' % (type, 'short.html'), data)
        encoded_data = simplejson.dumps({'message':rendered})

        for r in recipients:
            url = 'http://127.0.0.1/publish?id=notification_' + r.username
            try:
                urllib2.urlopen(url, encoded_data);
            except:
                pass


def push_message(recipient, data):
    if settings.LONGPOLL_ENABLED:
        encoded_data = simplejson.dumps(data)
        url = 'http://127.0.0.1/publish?id=message_' + recipient.username
        try:
            urllib2.urlopen(url, encoded_data);
        except:
            pass


def push_request(recipient, request):
    if settings.LONGPOLL_ENABLED:
        data = {
            'from_user':request.from_user.username,
            'message'  :request.message,
        }

        try:
            data['image_id'] = request.image.id
            data['location_id'] = request.location.id
        except:
            # we're allowed to pass because all but one will fail
            pass

        encoded_data = simplejson.dumps(data)
        url = 'http://127.0.0.1/publish?id=request_' + recipient.username
        try:
            urllib2.urlopen(url, encoded_data);
        except:
            pass

