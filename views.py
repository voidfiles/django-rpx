from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rpx.models import RpxData
import settings
TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS'), [])

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
        profile = json['profile']
        rpx_id = profile['identifier']
        nickname = profile.get('displayName') or \
          profile.get('preferredUsername')
        email = profile.get('email', '')
        profile_pic_url = profile.get('photo')
        info_page_url = profile.get('url')
        provider=profile.get("providerName")
        
        try:
            # are we aware of this rpx user already?
            user=User.objects.get(rpxdata__identifier=rpx_id)
        except User.DoesNotExist:
            # no. we can try to match on email, though, provided that doesn't steal
            # an rpx association
            
            if email and profile['providerName'] in TRUSTED_PROVIDERS:
                #beware - this would allow account theft, so we only allow it
                #for trusted providers
                user_candidates=User.objects.all().filter(
                  rpxdata=None).filter(email=email)
                # if unambiguous, do it. otherwise, don't.
                if user_candidates.count()==1:
                    [user]=user_candidates
            else:
                user=User.objects.create_user(nickname, email)
                rpxdata=RpxData(identifier=rpx_id)
                rpxdata.save()
                user.rpxdata=rpxdata
            
            if profile_pic_url:
                rpxdata.profile_pic_url=profile_pic_url
            if info_page_url:
                rpxdata.info_page_url=info_page_url
            if provider:
                rpxdata.provider=provider
            rpxdata.save()
        
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden()
