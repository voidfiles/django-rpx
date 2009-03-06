from django import template
from django.template import Context, loader
from django.template.loader import render_to_string
import settings
from django.core.urlresolvers import reverse

"""
"rpx_tags" is a slightly redundant name, but if i clall this module simple "rpx" it only allows me to use the first tag found (although all tags appear in the libary)

weird.
"""

register = template.Library()


# @register.simple_tag
# def rpx_link(text):
#     return render_to_string('rpx_link.html',  {
#       'text': text,
#       'realm': settings.RPXNOW_REALM,
#       'token_url': "http://%s%s" % (settings.HOST, reverse('rpx.views.rpx_response'))
#     })
@register.inclusion_tag('rpx_link.html', takes_context=True)
def rpx_link(context, text):
    return {
      'text': text,
      'realm': settings.RPXNOW_REALM,
      'token_url': "http://%s%s" % (settings.HOST, reverse('rpx.views.rpx_response'))
    }
    
"""
<a class="rpxnow" onclick="return false;"
   href="https://{{ realm }}.rpxnow.com/openid/v2/signin?token_url={{ token_url }}">
  {{ text }}
</a>
"""

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