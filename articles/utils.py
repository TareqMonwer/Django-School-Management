import requests
import json
from django.conf import settings

if settings.USE_MAILCHIMP:
    MAILCHIMP_API_KEY=settings.MAILCHIMP_API_KEY
    MAILCHIMP_DATA_CENTER=settings.MAILCHIMP_DATA_CENTER
    MAILCHIMP_LIST_ID = settings.MAILCHIMP_LIST_ID

    API_URL = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
    memebers_endpoint = f'{API_URL}/lists/{MAILCHIMP_LIST_ID}/members'

def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    try:
        r = requests.post(
            memebers_endpoint,
            auth=("", MAILCHIMP_API_KEY),
            data=json.dumps(data)
        )
        return r.status_code, r.json()
    except:
        raise Exception("Mailchimp is not configured properly.")