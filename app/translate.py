try:
  import httplib  # Python 2
except ImportError:
  import http.client as httplib  # Python 3
try:
  from urllib import urlencode  # Python 2
except ImportError:
  from urllib.parse import urlencode  # Python 3

import requests
import json

from flask.ext.babel import gettext

from config import MS_TRANSLATOR_CLIENT_ID, MS_TRANSLATOR_CLIENT_SECRET


def microsoft_translate(text, sourceLang, destLang):
  """Translate text using Microsoft Translate API:
  https://www.microsoft.com/translator/getstarted.aspx
  """
  if MS_TRANSLATOR_CLIENT_ID == '' or MS_TRANSLATOR_CLIENT_SECRET == '':
    return gettext('Error: translation service not configured.')
  try:
    # get access token
    params = urlencode({
      'client_id': MS_TRANSLATOR_CLIENT_ID,
      'client_secret': MS_TRANSLATOR_CLIENT_SECRET,
      'scope': 'http://api.microsofttranslator.com',
      'grant_type': 'client_credentials'
    })
    conn = httplib.HTTPSConnection("datamarket.accesscontrol.windows.net")
    conn.request("POST", "/v2/OAuth2-13", params)
    response = json.loads(conn.getresponse().read())
    token = response[u'access_token']
  except Exception as err:
    return gettext("Error getting token: %s" % err)
  else:
    try:
      # translate
      url = 'http://api.microsofttranslator.com//V2/Ajax.svc/Translate'
      params = {
        'appId': 'Bearer ' + token,
        'from': sourceLang,
        'to': destLang,
        'text': text.encode("utf-8")
      }
      r = requests.get(url, params=params)

      # TODO(eso) json.loading currently doesn't work
      # response = json.loads("{\"response\":" + r.text.decode('utf-8') + "}")
      # return response["response"]

      print(r.text)
      return r.text
    except Exception as err:
      return gettext('Error getting translation: %s' % err)
