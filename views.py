from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def rpx_response(request):
    from django.utils import simplejson
    import urllib
    import urllib2
    token = request.get('token')
    url = 'https://rpxnow.com/api/v2/auth_info'
    args = {
      'format': 'json',
      'apiKey': settings.RPXNOW_API_KEY,
      'token': token
    }
    r = urllib2.urlopen(url=url,
      data=urllib.urlencode(args),
    )
    json = simplejson.load(r)
    if json['stat'] == 'ok':    
        unique_identifier = json['profile']['identifier']
        nickname = json['profile']['preferredUsername']
        email = json['profile']['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            """
            create a user
            """
            try:
                user_by_nick=User.objects.get(username=nickname)
                nickname="%s-%s"%(nickname, unique_identifier)
            except User.DoesNotExist:
                pass
            user=User.objects.create_user(nickname, email)
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden()