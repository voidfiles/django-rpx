from django import template
from django.template import Context, loader
import settings

"""
TODO: write a tag that create the login links too
"""

register = template.Library()

@register.inclusion_tag('rpx_script.html')
def rpx_script():
    return {
      'realm': settings.RPXNOW_REALM,
      'token_url': "http://%s%s" %(settings.HOST, reverse('rpx.views.rpx_response'))
    }
    
"""
put this in "rpx_script.html" in your templates dir.
<script src="https://rpxnow.com/openid/v2/widget"
        type="text/javascript"></script>
<script type="text/javascript">
  RPXNOW.token_url = "{{ token_url }}";
  RPXNOW.realm = "{{ realm }}";
  RPXNOW.overlay = true;
  RPXNOW.language_preference = 'en';
</script>
"""

@register.inclusion_tag('rpx_link.html')
def rpx_link(text):
    return {
      'text': text,
      'realm': settings.RPXNOW_REALM,
      'token_url': "http://%s%s" %(settings.HOST, reverse('rpx.views.rpx_response'))
    }
    
"""
<a class="rpxnow" onclick="return false;"
   href="https://{{ realm }}.rpxnow.com/openid/v2/signin?token_url=http://{{ host }}{% url rpx.views.rpx_response %}">
  {{ text }}
</a>
"""