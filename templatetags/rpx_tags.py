from django import template
from django.template import Context, loader
from django.template.loader import render_to_string
import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
"""
"rpx_tags" is a slightly redundant name, but if i clall this module simple "rpx" it only allows me to use the first tag found (although all tags appear in the libary)

weird.

Anyway.

TODO:
  * provide for language choice
  * document
  * provide for customisation for the "overlay" attribute, whatever it is.

"""

register = template.Library()

@register.inclusion_tag('rpx_link.html', takes_context=True)
def rpx_link(context, text):
    current_site=Site.objects.get_current()
    
    return {
      'text': text,
      'realm': settings.RPXNOW_REALM,
      'token_url': "http://%s%s" % (current_site.domain,
        reverse('rpx.views.rpx_response'))
    }
    
"""
put this in "rpx_script.html" in your templates dir.
<a class="rpxnow" onclick="return false;"
   href="https://{{ realm }}.rpxnow.com/openid/v2/signin?token_url={{ token_url }}">
  {{ text }}
</a>
"""

@register.inclusion_tag('rpx_script.html')
def rpx_script():
    current_site=Site.objects.get_current()
    
    return {
      'realm': settings.RPXNOW_REALM,
      'token_url': "http://%s%s" %(current_site.domain,
        reverse('rpx.views.rpx_response'))
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