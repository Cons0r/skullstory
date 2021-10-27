import hashlib
import requests
import os
import datetime

def now():
  return datetime.datetime.now()
def genergrav(email):
  hashmail = hashlib.md5(str(email).strip().lower().encode()).hexdigest()
  return f'https://www.gravatar.com/avatar/{hashmail}?s=25'
def report(text):
  req = requests.post('https://api.sightengine.com/1.0/text/check.json', {
    'text': text,
    'mode': 'standard',
    'api_user': 30541851,
    'api_secret': os.environ['api secret'],
    'lang':'en'}).json()
  if len(req['profanity']['matches']) > 0:
    return True
  elif len(req['personal']['matches']) > 0:
    return True
  elif len(req['link']['matches']) > 0:
    return True
  else:
    return False