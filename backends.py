from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rpx.models import RpxData
import settings
TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class RpxBackend:
    def get_user(self, rpx_id):
        try:
            return User.objects.get(rpxdata__identifier=rpx_id)
        except User.DoesNotExist:
            return None
                
    def authenticate(self, token=''):
        from django.utils import simplejson
        import urllib
        import urllib2

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
        if json['stat'] <> 'ok':
            return HttpResponseForbidden()
        profile = json['profile']
        rpx_id = profile['identifier']
        nickname = profile.get('displayName') or \
          profile.get('preferredUsername')
        email = profile.get('email', '')
        profile_pic_url = profile.get('photo')
        info_page_url = profile.get('url')
        provider=profile.get("providerName")

        user=self.get_user(rpx_id)
        
        if not user:
            # no match. we can try to match on email, though, provided that doesn't steal
            # an rpx association
            import pdb; pdb.set_trace()
            if email and profile['providerName'] in TRUSTED_PROVIDERS:
                #beware - this would allow account theft, so we only allow it
                #for trusted providers
                user_candidates=User.objects.all().filter(
                  rpxdata=None).filter(email=email)
                # if unambiguous, do it. otherwise, don't.
                if user_candidates.count()==1:
                    [user]=user_candidates
            else: #no match, create a new user - but there may be duplicates
                username=nickname
                try:
                    i=0
                    while True:
                        User.objects.get(username=username)
                        username=permute_name(nickname, i)
                        i+=1
                except User.DoesNotExist:
                    #available name!
                    user=User.objects.create_user(username, email)

                rpxdata=RpxData(identifier=rpx_id)
                rpxdata.user=user
                rpxdata.save()
        
        if profile_pic_url:
            rpxdata.profile_pic_url=profile_pic_url
        if info_page_url:
            rpxdata.info_page_url=info_page_url
        if provider:
            rpxdata.provider=provider
        rpxdata.save()
        return user